from plugin import Plugin
from utils import create_logger

import requests


class GitHub(Plugin):
    is_global = True
    log = create_logger('github')

    api_base_url = 'https://api.github.com'

    links = {}

    async def usage(self, message):
        usage = '```ruby\n'
        usage += 'Usage: {:s}gh <command>\n\n'.format(self.prefix)
        usage += 'commands:\n'
        usage += '  search <search query>\n'
        usage += '  link add|del|list <user/repo> [...]\n'
        usage += '```'
        await self.client.send_message(message.channel, usage)

    async def search(self, message, args):
        if args == []:
            await self.client.send_message(message.channel,
                'You need to add at least one search term')
            return

        query = ' '.join(args)

        url = '{:s}/search/repositories'.format(self.api_base_url)
        results = requests.get(url, params={'q': query})
        self.log.info('requested {:s}'.format(results.url))

        json_data = results.json()
        self.log.info(json_data)

        count = json_data['total_count']
        await self.client.send_message(message.channel,
                'Got {:d} results.'.format(count))

    def linkctl_add(self, repos):
        out = ''
        # FIXME: check for repo validity
        # TODO: save repos in db
        for repo_path in repos:
            user, repo = repo_path.split('/')
            out += 'Adding link for repository **{:s}** from user **{:s}**\n'.format(repo, user)

        return out

    def linkctl_del(self, repos):
        out = ''
        # FIXME: check if repo is added
        for repo_path in repos:
            user, repo = repo_path.split('/')
            out += 'Removing link for repository **{:s}** from user **{:s}**\n'.format(repo, user)

        return out

    def linkctl_list(self):
        # TODO: get repos from db
        repos = []
        out = 'Gitub repositories:\n'
        for repo_path in repos:
            user, repo = repo_path.split('/')
            out += '**{:s}** from user **{:s}**\n'.format(repo, user)

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

        await self.client.send_message(message.channel, out)

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
