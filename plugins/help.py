from plugin import Plugin
from config import *
from utils import bold
from utils import create_logger
import asyncio


class Help(Plugin):
    is_global = True
    log = create_logger(cmd_help)

    async def on_message(self, message, pfx):
        if message.content == (pfx + cmd_help):
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
            try:
                await self.client.delete_message(help_msg)
            except:
                print('Help Message Deletion Failed - Not found or something...')
                pass
        elif message.content.startswith(pfx + cmd_help + ' '):
            cmd_name = 'Command Help'
            self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                          message.author,
                          message.author.id, message.server.name, message.server.id, message.channel)
            await self.client.send_typing(message.channel)
            help_q = str(message.content[len(pfx) + len(cmd_help) + 1:])
            q = help_q.lower()
            if q == "bns" or q == "blade and soul":
                desc = desc_bns
                usg = usg_bns
                out_type = 0
            elif q == 'echo':
                desc = desc_echo
                usg = usg_echo
                out_type = 0
            elif q == 'gelbooru':
                desc = desc_gelbooru
                usg = usg_gelbooru
                out_type = 0
            elif q == 'hearthstone' or q == 'hs':
                desc = desc_hearthstone
                usg = usg_hearthstone
                out_type = 0
            elif q == 'imdb':
                desc = desc_imdb
                usg = usg_imdb
                out_type = 0
            elif q == 'itad':
                desc = desc_itad
                usg = usg_itad
                out_type = 0
            elif q == 'joke':
                desc = desc_joke
                usg = usg_joke
                out_type = 0
            else:
                desc = 'None'
                usg = 'None'
                out_type = 1
            if out_type == 1:
                out_text = 'Command not found or not specified...'
            else:
                out_text = (bold('Description:') + '\n```java\n' + desc + '\n```\n' + bold('Usage: ') + '`' + usg + '`')
            await self.client.send_message(message.channel, out_text)
