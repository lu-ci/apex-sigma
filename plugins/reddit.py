from plugin import Plugin
from utils import create_logger
import praw
import random
import asyncio
from config import OwnerID as ownr

mmm = False


class FoodPorn(Plugin):
    is_global = True
    log = create_logger('food_porn')

    async def on_message(self, message, pfx):
        if message.content.startswith(pfx + 'foodporn'):
            await self.client.send_typing(message.channel)
            cmd_name = 'Food Porn'
            try:
                self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                              message.author,
                              message.author.id, message.server.name, message.server.id, message.channel)
            except:
                self.log.info('User %s [%s], used the ' + cmd_name + ' command.',
                              message.author,
                              message.author.id)
            if mmm is False:
                try:
                    global mmm
                    time_choice = int(message.content[len(pfx) + len('foodporn') + 1:])
                    if message.author.id == ownr:
                        mmm = True
                        while mmm is True:
                            req = praw.Reddit(user_agent='Apex Sigma')
                            posts = req.get_subreddit('foodporn').get_hot(limit=100)
                            url_list = []
                            for post in posts:
                                url_list.append(post.url)
                            out = random.choice(url_list)
                            await self.client.send_message(message.channel, out)
                            await asyncio.sleep(time_choice)
                    else:
                        await self.client.send_message(message.channel,
                                                       'Insufficient permissions...\nOnly <@' + ownr + '> can activate the ' + cmd_name + ' command~')
                except:
                    await self.client.send_message(message.channel, 'Not a number or something went to shit...')
            elif mmm is not False:
                if message.author.id == ownr:
                    mmm = False
                    await self.client.send_message(message.channel, 'Loop stopped...')
                else:
                    await self.client.send_message(message.channel,
                                                   'Insufficient permissions...\nOnly <@' + ownr + '> can activate the ' + cmd_name + ' command~')
