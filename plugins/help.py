from plugin import Plugin
from config import *
from utils import create_logger
import asyncio


class Help(Plugin):
    is_global = True
    log = create_logger(cmd_help)

    async def on_message(self, message, pfx):
        if message.content.startswith(pfx + cmd_help):
            cmd_name = 'Help'
            self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                          message.author,
                          message.author.id, message.server.name, message.server.id, message.channel)
            await self.client.send_typing(message.channel)
            help_msg = await self.client.send_message(message.channel, '```\nHelp: ' + pfx + cmd_help +
                                                      '\nOverwatch: ' + pfx + cmd_overwatch +
                                                      '\nLeague of Legends: ' + pfx + cmd_league +
                                                      '\nBlade and Soul: ' + pfx + cmd_bns +
                                                      '\n - Detailed Attack Stats: ' + pfx + cmd_bns_att +
                                                      '\n - Detailed Defense Stats: ' + pfx + cmd_bns_def +
                                                      '\nOsu! Profile: ' + pfx + cmd_osu +
                                                      '\nUrban Dictionary: ' + pfx + cmd_ud +
                                                      '\nWeather: ' + pfx + cmd_weather +
                                                      '\nHearthstone: ' + pfx + cmd_hearthstone +
                                                      '\nPokemon: ' + pfx + cmd_pokemon +
                                                      '\nJoke: ' + pfx + cmd_joke +
                                                      '\nLastFM: ' + pfx + cmd_lfm +
                                                      '\nNSFW Permission: ' + pfx + cmd_nsfw_permit +
                                                      '\nGelbooru: ' + pfx + cmd_gelbooru +
                                                      '\nRule34: ' + pfx + cmd_rule34 +
                                                      '\nnHentai: ' + pfx + cmd_nhentai +
                                                      '\nAnime Search: ' + pfx + cmd_anime +
                                                      '\nManga Search: ' + pfx + cmd_manga +
                                                      '\nJisho: ' + pfx + cmd_jisho +
                                                      '\nWaniKani: ' + pfx + cmd_wk +
                                                      '\nWaniKani Key Save: ' + pfx + cmd_wk_store +
                                                      '\nIsThereAnyDeal: ' + pfx + cmd_itad +
                                                      '\nIMDB: ' + pfx + cmd_imdb +
                                                      '\nEnchant Scroll Search: ' + pfx + cmd_vindi +
                                                      '\n```' +
                                                      '\nMade by `Alex` with **love**!\nhttps://github.com/AXAz0r/apex-sigma')
            await asyncio.sleep(60)
            await self.client.delete_message(help_msg)
            # print('CMD [' + cmd_name + '] > ' + initiator_data)
