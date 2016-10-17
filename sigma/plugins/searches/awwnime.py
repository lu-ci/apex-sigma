from sigma.plugin import Plugin
from sigma.utils import create_logger
import praw
import random


class Awwnime(Plugin):

    is_global = True
    log = create_logger('awwnime')

    async def on_message(self, message, pfx):
        if message.content == pfx + 'awwnime':
            await self.client.send_typing(message.channel)
            cmd_name = 'Awwnime'
            try:
                self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                              message.author,
                              message.author.id, message.server.name, message.server.id, message.channel)
            except:
                self.log.info('User %s [%s], used the ' + cmd_name + ' command.',
                              message.author,
                              message.author.id)
            req = praw.Reddit(user_agent='Apex Sigma')
            posts = req.get_subreddit('awwnime').get_hot(limit=100)
            url_list = []
            for post in posts:
                url_list.append(post.url)
            out_tex = random.choice(url_list)
            await self.reply(out_tex)
