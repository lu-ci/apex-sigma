import requests
import json
import logging
import threading

import tornado.ioloop
import tornado.web

from sigma.plugin import Plugin
from sigma.utils import create_logger

from config import GitHubWebserverPort as gh_port
from config import GitHubWebserverAddr as gh_addr


# GitHub event handlers and links
event_handlers = {}
channel_links = {}


class Payload():
    def __init__(self, payload):
        self.data = payload

    def repo_name(self):
        self.data['repository']['full_name']

    def sender_name(self):
        self.data['sender']['login']

    def issue(self):
        self.data['issue']

    def pull_request(self):
        self.data['pull_request']

    def small_issue(self):
        'Small issue'

    def small_pull_request(self):
        'Small pull request'

    def action(self):
        self.data['action']


def handle_event(evtype, payload):
    payload = Payload(payload)

    if event_handlers[evtype]:
        event_handlers[evtype].handle(payload)


# Web server stuff
class WebMainHandler(tornado.web.RequestHandler):
    async def get(self):
        self.write('Sigma<br>')

    async def post(self):
        event_type = self.request.headers.get('X-GitHub-Event')
        payload = json.loads(self.request.body.decode('utf-8'))
        repo_name = payload['repository']['full_name']

        channels = channel_links[repo_name]
        for channel in channels:
            response = handle_event(event_type, payload)
            if response:
                pass


class WebServer(object):
    def __init__(self, plugin):
        self.bot = plugin.client
        self.log = plugin.log
        self.server = tornado.web.Application([
            (r'/webhook', WebMainHandler)
        ])
        self.server.listen(gh_port)
        logging.getLogger('tornado.access').addHandler(self.log)
        logging.getLogger('tornado.general').addHandler(self.log)
        logging.getLogger('tornado.application').addHandler(self.log)

        self.webthread = threading.Thread(target=self.ioloop)
        self.webthread.daemon = True

    def ioloop(self):
        tornado.ioloop.IOLoop.current().start()

    def run(self):
        self.webthread.start()
        self.log.info('Serving at localhost:{:d}'.format(gh_port))
        return self.webthread


# Main plugin class
class GitHub(Plugin):
    def __init__(self, client):
        super().__init__(client)

        self.is_global = True
        self.log = create_logger('github')
        self.api_base_url = 'https://api.github.com'
        self.links = {}
        self.webthread = WebServer(self).run()

    async def usage(self, message):
        usage = '```ruby\n'
        usage += 'Usage: {:s}gh <command>\n\n'.format(self.prefix)
        usage += 'commands:\n'
        usage += '  search <search query>\n'
        usage += '  link add|del|list <user/repo> [...]\n'
        usage += '```'
        await self.reply(usage)

    async def search(self, message, args):
        if args == []:
            await self.reply('You need to add at least one search term')
            return

        query = ' '.join(args)

        url = '{:s}/search/repositories'.format(self.api_base_url)
        results = requests.get(url, params={'q': query})
        self.log.info('requested {:s}'.format(results.url))

        json_data = results.json()
        self.log.info(json_data)

        count = json_data['total_count']
        await self.reply('Got {:d} results.'.format(count))

    def linkctl_add(self, repos):
        out = ''
        # FIXME: check for repo validity
        for repo_path in repos:
            user, repo = repo_path.split('/')
            out += 'Adding link for repository **{:s}** from user **{:s}**\n'.format(repo, user)

            query = 'SELECT ID, CHANNELS FROM GITHUB_LINKS WHERE GH_USER=? AND GH_REPO=?'
            response = self.db.execute(query, user, repo)
            response = response.fetchone()

            id = None
            channels = None

            if response:
                id, channels = response

            self.log.info('{:} {:}'.format(id, channels))

            if id:
                channels = str(channels).split(',')
                self.log.info(channels)

                if channels.count(self.channel.id) == 0:
                    self.log.info('adding current channel')
                    channels.append(str(self.channel.id))
                else:
                    self.log.info('current channel already in database')
                    return

                channels = ','.join(channels)
                self.log.info(channels)

                query = 'UPDATE GITHUB_LINKS SET CHANNELS=? WHERE ID=?'
                self.db.execute(query, channels, id)
                self.db.commit()
            else:
                self.log.info('adding link to repo {:s}/{:s} for channel {:s}'.format(user, repo, self.channel.name))
                query = 'INSERT INTO GITHUB_LINKS(ADDED_BY, ADDED_DATE, GH_USER, GH_REPO, CHANNELS) VALUES (?, ?, ?, ?, ?)'
                self.db.execute(query, self.author.id, 1, user, repo, self.channel.id)
                self.db.commit()

        return out

    def linkctl_del(self, repos):
        out = ''
        # FIXME: check if repo is added
        for repo_path in repos:
            user, repo = repo_path.split('/')
            out += 'Removing link for repository **{:s}** from user **{:s}**\n'.format(repo, user)

        return out

    def linkctl_list(self):

        query = 'SELECT ALL GH_USER, GH_REPO FROM GITHUB_LINKS WHERE CHANNELS GLOB ?'
        response = self.db.execute(query, '*{:s}*'.format(self.channel.id))
        response = response.fetchall()

        if response:
            out = 'GitHub repositories linked to this channel:\n'
            for (user, repo) in response:
                out += '**{:s}**/**{:s}**\n'.format(user, repo)

            return out

    async def linkctl(self, message, args):
        if not args:
            self.usage()
            return

        subcmd = args.pop(0)
        repos = args

        out = ''
        if subcmd == 'add':
            out = self.linkctl_add(repos)
        elif subcmd == 'del':
            out = self.linkctl_del(repos)
        elif subcmd == 'list':
            out = self.linkctl_list()
        else:
            out = 'Unknown command: {:s}'.format(subcmd)
            await self.usage(message)

        await self.reply(out)

    async def webserverctl(self, message, args):
        if args == []:
            await self.usage(message)
            return

        cmd = args.pop(0)

        if cmd == 'status':
            online = 'online' if self.webthread.is_alive() else 'offline'
            msg = 'Webserver:\n\tStatus: {:s}\n\tAddress: {:s}'.format(online, gh_addr)
            await self.reply(msg)
        else:
            await self.usage(message)

    async def on_message(self, message, pfx=''):
        if message.content.startswith(self.prefix + 'gh'):
            await self.client.send_typing(message.channel)

            args = message.content.split(' ')
            self.log.info(args)
            args.pop(0)

            if not args:
                await self.usage(message)
                return

            subcmd = args.pop(0)

            if subcmd == 'search':
                await self.search(message, args)
            elif subcmd == 'link':
                await self.linkctl(message, args)
            elif subcmd == 'websrv':
                await self.webserverctl(message, args)
            else:
                await self.usage(message)
