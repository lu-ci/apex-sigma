from sigma.plugin import Plugin
from sigma.utils import create_logger
import praw
import random


class Reddit(Plugin):

    is_global = True
    log = create_logger('reddit')

    async def on_message(self, message, pfx):
        if message.content.startswith(pfx + 'reddit '):
            await self.client.send_typing(message.channel)
            cmd_name = 'Reddit'
            try:
                self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                              message.author,
                              message.author.id, message.server.name, message.server.id, message.channel)
            except:
                self.log.info('User %s [%s], used the ' + cmd_name + ' command.',
                              message.author,
                              message.author.id)
            q = message.content[len(pfx) + len('reddit') + 1:]
            req = praw.Reddit(user_agent='Apex Sigma')
            try:
                posts = req.get_subreddit(str(q)).get_hot(limit=100)
                url_list = []
                for post in posts:
                    url_list.append(post.url)
                out_tex = random.choice(url_list)
                await self.reply(out_tex)
            except Exception as err:
                await self.reply(str(err))
