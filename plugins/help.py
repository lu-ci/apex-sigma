from plugin import Plugin
from config import *
from utils import create_logger
import asyncio


class Help(Plugin):
    is_global = True
    log = create_logger(cmd_help)

    async def on_message(self, message, pfx):
        if message.content.startswith(pfx + cmd_help):
            cmd_name = 'Module List'
            self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                          message.author,
                          message.author.id, message.server.name, message.server.id, message.channel)
            await self.client.send_typing(message.channel)
            help_msg = await self.client.send_message(message.channel, '```java' +
                                                      '\n\"Help\": ' + pfx + cmd_help +
                                                      '\n\"Overwatch\": ' + pfx + cmd_overwatch +
                                                      '\n\"League of Legends\": ' + pfx + cmd_league +
                                                      '\n\"Blade and Soul\": ' + pfx + cmd_bns +
                                                      '\n\"Osu! Profile\": ' + pfx + cmd_osu +
                                                      '\n\"Urban Dictionary\": ' + pfx + cmd_ud +
                                                      '\n\"Weather\": ' + pfx + cmd_weather +
                                                      '\n\"Hearthstone\": ' + pfx + cmd_hearthstone +
                                                      '\n\"Pokemon\": ' + pfx + cmd_pokemon +
                                                      '\n\"Joke\": ' + pfx + cmd_joke +
                                                      '\n\"LastFM\": ' + pfx + cmd_lfm +
                                                      '\n\"NSFW Permission\": ' + pfx + cmd_nsfw_permit +
                                                      '\n\"Gelbooru\": ' + pfx + cmd_gelbooru +
                                                      '\n\"Rule34\": ' + pfx + cmd_rule34 +
                                                      '\n\"nHentai\": ' + pfx + cmd_nhentai +
                                                      '\n\"Anime Search\": ' + pfx + cmd_anime +
                                                      '\n\"Manga Search\": ' + pfx + cmd_manga +
                                                      '\n\"Jisho\": ' + pfx + cmd_jisho +
                                                      '\n\"WaniKani\": ' + pfx + cmd_wk +
                                                      '\n\"WaniKani Key Save\": ' + pfx + cmd_wk_store +
                                                      '\n\"IsThereAnyDeal\": ' + pfx + cmd_itad +
                                                      '\n\"IMDB\": ' + pfx + cmd_imdb +
                                                      '\n\"Enchant Scroll Search\": ' + pfx + cmd_vindi +
                                                      '\n```' +
                                                      '\nMade by `Alex` with **love**!\nhttps://github.com/AXAz0r/apex-sigma')
            await asyncio.sleep(60)
            await self.client.delete_message(help_msg)