from plugin import Plugin
from utils import create_logger
import praw
from config import reddit_un as un, reddit_pw as pw
import random
import asyncio
from config import OwnerID as ownr

logged_in = False


class Reddit(Plugin):
    is_global = True
    log = create_logger('Reddit')

    async def on_message(self, message, pfx):
        if message.content.startswith(pfx + 'redditlogin'):
            await self.client.send_typing(message.channel)
            cmd_name = 'Reddit Login'
            global logged_in
            # Start Logger
            try:
                self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                              message.author,
                              message.author.id, message.server.name, message.server.id, message.channel)
            except:
                self.log.info('User %s [%s], used the ' + cmd_name + ' command.',
                              message.author,
                              message.author.id)
            # Eng Logger
            if message.author.id == ownr:
                if logged_in is False:
                    conn = praw.Reddit(user_agent='Apex Sigma')
                    try:
                        conn.login(un, pw, disable_warning=True)
                    except praw.errors.InvalidUserPass:
                        await self.client.send_message(message.channel, 'Invalid Login Credentials')
                    await self.client.send_message(message.channel, 'Logged into Reddit as ' + un)
                    logged_in = True
                elif logged_in is not False:
                    await self.client.send_message(message.channel, 'Already logged in into Reddit as ' + un)
            else:
                await self.client.send_message(message.channel,
                                               'I\'m sorry <@' + message.author.id + '>, but you don\'t have that permission.')
        elif message.content.startswith(pfx + 'redditmulti'):
            mr = message.content[len(pfx) + len('redditmulti') + 1:]
            await self.client.send_typing(message.channel)
            cmd_name = 'Reddit Profile'
            # Start Logger
            try:
                self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                              message.author,
                              message.author.id, message.server.name, message.server.id, message.channel)
            except:
                self.log.info('User %s [%s], used the ' + cmd_name + ' command.',
                              message.author,
                              message.author.id)
            # Eng Logger
            conn = praw.Reddit(user_agent='Apex Sigma')
            try:
                multi = conn.get_multireddit('Imjustheretobefined', mr)
                multi_list = multi.get_hot(limit=10)
                out = ''
                for post in multi_list:
                    out += post.get_hot(limit=10)
                print(out)
                await self.client.send_message(message.channel, out)
            except SyntaxError:
                print('syn errrrrr')
