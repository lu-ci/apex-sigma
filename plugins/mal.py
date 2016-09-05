from plugin import Plugin
from config import cmd_mal
from utils import create_logger
from config import mal_un
from config import mal_pw
from lxml import html
import requests
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import os
from io import BytesIO
from requests.auth import HTTPBasicAuth


class MAL(Plugin):
    is_global = True
    log = create_logger(cmd_mal)

    async def on_message(self, message, pfx):
        if message.content.startswith(pfx + cmd_mal):
            await self.client.send_typing(message.channel)
            cmd_name = 'MyAnimeList'
            self.log.info('\nUser %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                          message.author,
                          message.author.id, message.server.name, message.server.id, message.channel)
            mal_input = message.content[len(pfx) + len(cmd_mal) + 1:]
            mal_url = 'https://myanimelist.net/api/anime/search.xml?q=' + mal_input
            mal = requests.get(mal_url, auth=HTTPBasicAuth(mal_un, mal_pw))
            entries = html.fromstring(mal.content)
            print(len(entries))
            n = 0
            list_text = 'List of anime found for `' + mal_input + '`:\n```'
            if len(entries) > 1:
                for entry in entries:
                    n +=1
                    list_text += '\n#' + str(n) + ' ' + entry[1].text
                await self.client.send_message(message.channel, list_text + '\n```\nPlease type the number corresponding to the anime of your choice `(1 - ' + str(len(entries)) + ')`')
                choice = await self.client.wait_for_message(author=message.author, channel=message.channel, timeout=20)
                try:
                    ani_no = int(choice.content) - 1
                except:
                    await self.client.send_message(message.channel, 'Not a number... Please start over')
                if choice is None:
                    return
            else:
                ani_no = 0
            try:
                ani_id = entries[ani_no][0].text
                name = entries[ani_no][1].text
                eps = entries[ani_no][4].text
                score = entries[ani_no][5].text
                air_start = (entries[ani_no][8].text)
                if air_start == '0000-00-00':
                    air_start = '???'
                air_end = (entries[ani_no][9].text)
                if air_end == '0000-00-00':
                    air_end = '???'
                air = air_start + ' to ' + air_end
                synopsis = (entries[ani_no][10].text).replace('[i]', '').replace('[/i]', '').replace('<br>', '').replace(
                    '</br>', '').replace('<br />', '').replace('&#039;', '\'').replace('&quot;', '"').replace('&mdash;',
                                                                                                              '-')
                img = entries[ani_no][11].text
                type = entries[ani_no][6].text
                status = entries[ani_no][7].text
                if len(name) > 22:
                    suffix = '...'
                else:
                    suffix = ''
                ani_img_raw = requests.get(img).content
                ani_img = Image.open(BytesIO(ani_img_raw))
                base = Image.open('img/ani/base.png')
                overlay = Image.open('img/ani/overlay.png')
                base.paste(ani_img, (0, 0))
                base.paste(overlay, (0, 0), overlay)
                font = ImageFont.truetype("big_noodle_titling_oblique.ttf", 28)
                imgdraw = ImageDraw.Draw(base)
                imgdraw.text((4, 4), '#' + ani_id, (255, 255, 255), font=font)
                imgdraw.text((227, 16), name[:21] + suffix, (255, 255, 255), font=font)
                imgdraw.text((227, 110), 'Type: ' + type, (255, 255, 255), font=font)
                imgdraw.text((227, 138), 'Status: ' + status, (255, 255, 255), font=font)
                imgdraw.text((227, 166), 'Episodes: ' + eps, (255, 255, 255), font=font)
                imgdraw.text((227, 194), 'Score: ' + score, (255, 255, 255), font=font)
                imgdraw.text((227, 222), air, (255, 255, 255), font=font)
                base.save('cache\\ani\\anime_' + message.author.id + '.png')
                await self.client.send_file(message.channel, 'cache\\ani\\anime_' + message.author.id + '.png')
                await self.client.send_message(message.channel, '```\n' + synopsis[
                                                                          :256] + '...\n\nMore At:\nhttps://myanimelist.net/anime/' + ani_id + '/ \n```')
                os.remove('cache\\ani\\anime_' + message.author.id + '.png')
            except IndexError:
                await self.client.send_message(message.channel, 'Number out of range, please start over...')
            except UnboundLocalError:
                pass
            except:
                await self.client.send_message(message.channel, 'Not found or API dun goofed...')
