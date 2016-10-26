import requests

from config import GitHubWebserverAddr as gh_addr


api_base_url = 'https://api.github.com'


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
