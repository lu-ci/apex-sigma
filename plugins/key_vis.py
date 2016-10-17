from plugin import Plugin
from utils import create_logger
import requests
from io import BytesIO
from PIL import Image
import random
import sqlite3


class KeyVisual(Plugin):
    is_global = True
    log = create_logger('keyvisualarts')

    async def on_message(self, message, pfx):
        # Lists Start
        key_vn_list = ['kud', 'air', 'knn', 'lbe', 'cla', 'pla', 'rhf', 'rwr']
        # List End
        if message.content == pfx + 'keyvis':
            await self.client.send_typing(message.channel)
            cmd_name = 'Key Visual Random'
            dbsql = sqlite3.connect('storage/server_settings.sqlite', timeout=20)
            try:
                self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                              message.author,
                              message.author.id, message.server.name, message.server.id, message.channel)
            except:
                self.log.info('User %s [%s], used the ' + cmd_name + ' command.',
                              message.author,
                              message.author.id)
            try:
                ch_id = (str(message.channel.id),)
                perms = dbsql.execute("SELECT PERMITTED from NSFW where CHANNEL_ID=?;", ch_id)
                permed = 'No'
                for row in perms:
                    permed = row[0]
            except sqlite3.OperationalError:
                permed = 'No'
            except Exception as err:
                print(err)
                permed = 'No'
            if permed == 'Yes':
                permitted = True
            else:
                permitted = False
            # End Perms
            if permitted is True:
                ran_chosen = random.choice(key_vn_list)
                if ran_chosen == 'kud':
                    end_range = 290
                elif ran_chosen == 'air':
                    end_range = 156
                elif ran_chosen == 'knn':
                    end_range = 175
                elif ran_chosen == 'lbe':
                    end_range = 424
                elif ran_chosen == 'cla':
                    end_range = 206
                elif ran_chosen == 'pla':
                    end_range = 19
                elif ran_chosen == 'rhf':
                    end_range = 84
                elif ran_chosen == 'rwr':
                    end_range = 252
                else:
                    return
                ran_image_number = random.randint(1, end_range)
                random_number_length = len(str(ran_image_number))
                ran_image_chosen = '0000'[:-random_number_length] + str(ran_image_number)
                image_url = 'https://cgv.blicky.net/%series%/%image%.jpg'.replace('%series%', ran_chosen).replace(
                    '%image%', ran_image_chosen)
                await self.client.send_message(message.channel, image_url)
            else:
                await self.client.send_message(message.channel,
                                               'This channel does not have the NSFW Module permitted!')
        elif message.content.startswith(pfx + 'keyvis '):
            await self.client.send_typing(message.channel)
            cmd_name = 'Key Visual by Choice'
            dbsql = sqlite3.connect('storage/server_settings.sqlite', timeout=20)
            try:
                self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                              message.author,
                              message.author.id, message.server.name, message.server.id, message.channel)
            except:
                self.log.info('User %s [%s], used the ' + cmd_name + ' command.',
                              message.author,
                              message.author.id)
            try:
                ch_id = (str(message.channel.id),)
                perms = dbsql.execute("SELECT PERMITTED from NSFW where CHANNEL_ID=?;", ch_id)
                permed = 'No'
                for row in perms:
                   permed = row[0]
            except sqlite3.OperationalError:
                permed = 'No'
            except Exception as err:
                print(err)
                permed = 'No'
            if permed == 'Yes':
                permitted = True
            else:
                permitted = False
            # End Perms
            if permitted is True:
                q = message.content[len(pfx) + len('keyvis'):].lower()
                if 'kud' in q:
                    visual_abrev = 'kud'
                elif 'air' in q:
                    visual_abrev = 'air'
                elif 'kanon' in q:
                    visual_abrev = 'knn'
                elif 'little' in q:
                    visual_abrev = 'lbe'
                elif 'clan' in q:
                    visual_abrev = 'cla'
                elif 'plane' in q:
                    visual_abrev = 'pla'
                elif 'harv' in q:
                    visual_abrev = 'rhf'
                elif 'rewr' in q and ('harv' not in q or 'fest' not in q):
                    visual_abrev = 'rwr'
                elif q in key_vn_list:
                    visual_abrev = q
                else:
                    await self.client.send_message(message.channel, 'Nothing found for `' + str(q) + '`...')
                    return
                url_base = 'https://cgv.blicky.net/'
                if visual_abrev == 'kud':
                    end_range = 290
                elif visual_abrev == 'air':
                    end_range = 156
                elif visual_abrev == 'knn':
                    end_range = 175
                elif visual_abrev == 'lbe':
                    end_range = 424
                elif visual_abrev == 'cla':
                    end_range = 206
                elif visual_abrev == 'pla':
                    end_range = 19
                elif visual_abrev == 'rhf':
                    end_range = 84
                elif visual_abrev == 'rwr':
                    end_range = 252
                else:
                    return
                ran_image_number = random.randint(1, end_range)
                random_number_length = len(str(ran_image_number))
                ran_image_chosen = '0000'[:-random_number_length] + str(ran_image_number)
                image_url = url_base + visual_abrev + '/' + ran_image_chosen + '.jpg'
                await self.client.send_message(message.channel, image_url)
            else:
                await self.client.send_message(message.channel,
                                               'This channel does not have the NSFW Module permitted!')
