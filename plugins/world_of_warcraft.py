from plugin import Plugin
from config import cmd_wow_character
from config import BlizzardKey
import requests
from utils import create_logger
import os
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO


class World_Of_Warcraft(Plugin):
    is_global = True
    log = create_logger('wow')

    async def on_message(self, message, pfx):
        if message.content.startswith(pfx + cmd_wow_character + ' '):
            cmd_name = 'WoW Character'
            try:
                self.log.info(
                    'User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                    message.author,
                    message.author.id, message.server.name, message.server.id, message.channel)
            except:
                self.log.info('User %s [%s], used the ' + cmd_name + ' command.',
                              message.author,
                              message.author.id)
            await self.client.send_typing(message.channel)
            query = message.content[len(pfx) + len(cmd_wow_character) + 1:]
            try:
                region_raw, realm, char_name = query.split(maxsplit=2)
            except:
                await self.client.send_message(message.channel, 'Invalid Input Format, please reffer to the example:\n`' + pfx + cmd_wow_character + ' EU Doomhammer Takamatsuku`')
                return
            try:
                region = region_raw.replace('_', '%20')
                base_url = 'https://' + region.lower() + '.api.battle.net/wow/character/' + realm + '/' + char_name + '?locale=en_GB&apikey=' + BlizzardKey
                char_data = requests.get(base_url).json()
                achi_url = 'https://' + region.lower() + '.api.battle.net/wow/character/' + realm + '/' + char_name + '?fields=achievements' + '&locale=en_GB&apikey=' + BlizzardKey
                achi_data = requests.get(achi_url).json()
                items_url = 'https://' + region.lower() + '.api.battle.net/wow/character/' + realm + '/' + char_name + '?fields=items' + '&locale=en_GB&apikey=' + BlizzardKey
                items_data = requests.get(items_url).json()
                # Character Data Begin
                char_ig_name = char_data['name']
                char_realm = char_data['realm']
                battlegroup = char_data['battlegroup']
                race_id = char_data['race']
                if race_id == 1:
                    race_name = 'Human'
                elif race_id == 2:
                    race_name = 'Orc'
                elif race_id == 3:
                    race_name = 'Dwarf'
                elif race_id == 4:
                    race_name = 'Night Elf'
                elif race_id == 5:
                    race_name = 'Undead'
                elif race_id == 6:
                    race_name = 'Tauren'
                elif race_id == 7:
                    race_name = 'Gnome'
                elif race_id == 8:
                    race_name = 'Troll'
                elif race_id == 9:
                    race_name = 'Goblin'
                elif race_id == 10:
                    race_name = 'Blood Elf'
                elif race_id == 11:
                    race_name = 'Draenei'
                elif race_id == 22:
                    race_name = 'Worgen'
                elif race_id == 24:
                    race_name = 'Pandaren'
                elif race_id == 25:
                    race_name = 'Pandaren'
                elif race_id == 26:
                    race_name = 'Pandaren'
                else:
                    race_name = 'Error'
                # -------
                class_id = char_data['class']
                if class_id == 1:
                    class_name = 'Warrior'
                elif class_id == 2:
                    class_name = 'Paladin'
                elif class_id == 3:
                    class_name = 'Hunter'
                elif class_id == 4:
                    class_name = 'Rogue'
                elif class_id == 5:
                    class_name = 'Priest'
                elif class_id == 6:
                    class_name = 'Death Knight'
                elif class_id == 7:
                    class_name = 'Shaman'
                elif class_id == 8:
                    class_name = 'Mage'
                elif class_id == 9:
                    class_name = 'Warlock'
                elif class_id == 10:
                    class_name = 'Monk'
                elif class_id == 11:
                    class_name = 'Druid'
                elif class_id == 12:
                    class_name = 'Demon Hunter'
                # -------

                gender_id = char_data['gender']
                if gender_id == 1:
                    gender_name = 'Female'
                else:
                    gender_name = 'Male'
                char_level = char_data['level']
                char_achi_points = char_data['achievementPoints']
                thumbnail = char_data['thumbnail']
                faction = char_data['faction']
                if faction == 1:
                    faction_name = 'Horde'
                elif faction == 0:
                    faction_name = 'Alliance'
                else:
                    faction_name = 'Neutral'
                hon_kills = char_data['totalHonorableKills']
                image_url = 'http://' + region.lower() + '.battle.net/static-render/' + region.lower() + '/' + thumbnail
                # Character Data End
                # Achievement Data Start
                achi_no = len(achi_data['achievements']['achievementsCompleted'])
                # Achievement Data End
                # Item Data Start
                avg_item_level = items_data['items']['averageItemLevel']
                try:
                    item_head = items_data['items']['head']['name']
                except:
                    item_head = 'None'
                try:
                    item_neck = items_data['items']['neck']['name']
                except:
                    item_neck = 'None'
                try:
                    item_shoulder = items_data['items']['shoulder']['name']
                except:
                    item_shoulder = 'None'
                try:
                    item_back = items_data['items']['back']['name']
                except:
                    item_back = 'None'
                try:
                    item_chest = items_data['items']['chest']['name']
                except:
                    item_chest = 'None'
                try:
                    item_shirt = items_data['items']['shirt']['name']
                except:
                    item_shirt = 'None'
                try:
                    item_tabard = items_data['items']['tabard']['name']
                except:
                    item_tabard = 'None'
                try:
                    item_wrist = items_data['items']['wrist']['name']
                except:
                    item_wrist = 'None'
                try:
                    item_hands = items_data['items']['hands']['name']
                except:
                    item_hands = 'None'
                try:
                    item_waist = items_data['items']['waist']['name']
                except:
                    item_waist = 'None'
                try:
                    item_legs = items_data['items']['legs']['name']
                except:
                    item_legs = 'None'
                try:
                    item_feet = items_data['items']['feet']['name']
                except:
                    item_feet = 'None'
                try:
                    item_finger1 = items_data['items']['finger1']['name']
                except:
                    item_finger1 = 'None'
                try:
                    item_finger2 = items_data['items']['finger2']['name']
                except:
                    item_finger2 = 'None'
                try:
                    item_trinket1 = items_data['items']['trinket1']['name']
                except:
                    item_trinket1 = 'None'
                try:
                    item_trinket2 = items_data['items']['trinket2']['name']
                except:
                    item_trinket2 = 'None'
                try:
                    item_main_hand = items_data['items']['mainHand']['name']
                except:
                    item_main_hand = 'None'
                try:
                    item_off_hand = items_data['items']['offHand']['name']
                except:
                    item_off_hand = 'None'
                # Item Data End

                base = Image.open('img/wow/base_wow.png')
                overlay = Image.open('img/wow/overlay_wow.png')
                base.paste(overlay, (0, 0), overlay)
                font1 = ImageFont.truetype("big_noodle_titling_oblique.ttf", 64)
                font2 = ImageFont.truetype("big_noodle_titling_oblique.ttf", 30)
                font3 = ImageFont.truetype("big_noodle_titling_oblique.ttf", 87)
                font4 = ImageFont.truetype("big_noodle_titling_oblique.ttf", 28)
                imgdraw = ImageDraw.Draw(base)
                imgdraw.text((5, 2), char_ig_name, (255, 255, 255), font=font1)
                imgdraw.text((5, 64), race_name + ' ' + class_name + ' of ' + char_realm, (255, 255, 255), font=font2)
                imgdraw.text((633, 2), str(char_level), (255, 255, 255), font=font3)
                imgdraw.text((100, 104), item_head, (255, 255, 255), font=font4)
                imgdraw.text((100, 131), item_neck, (255, 255, 255), font=font4)
                imgdraw.text((100, 158), item_shoulder, (255, 255, 255), font=font4)
                imgdraw.text((100, 185), item_back, (255, 255, 255), font=font4)
                imgdraw.text((100, 212), item_chest, (255, 255, 255), font=font4)
                imgdraw.text((100, 239), item_shirt, (255, 255, 255), font=font4)
                imgdraw.text((100, 266), item_tabard, (255, 255, 255), font=font4)
                imgdraw.text((100, 293), item_wrist, (255, 255, 255), font=font4)
                imgdraw.text((100, 320), item_hands, (255, 255, 255), font=font4)
                imgdraw.text((100, 347), item_waist, (255, 255, 255), font=font4)
                imgdraw.text((100, 374), item_legs, (255, 255, 255), font=font4)
                imgdraw.text((100, 401), item_feet, (255, 255, 255), font=font4)
                imgdraw.text((100, 428), item_finger1, (255, 255, 255), font=font4)
                imgdraw.text((100, 455), item_finger2, (255, 255, 255), font=font4)
                imgdraw.text((100, 482), item_trinket1, (255, 255, 255), font=font4)
                imgdraw.text((100, 509), item_trinket2, (255, 255, 255), font=font4)

                base.save('cache\\wow_' + message.author.id + '.png')
                await self.client.send_file(message.channel, 'cache/wow_' + message.author.id + '.png')
                os.remove('cache\\wow_' + message.author.id + '.png')
            except:
                try:
                    error_no = char_data['status']
                    error_msg = char_data['reason']
                    await self.client.send_message(message.channel, 'Error: ' + str(error_no) + '\n' + error_msg)
                except:
                    await self.client.send_message(message.channel, 'Something went wrong, most likely invalid region...\nRegions are: `US`, `EU`, `KR`, `TW`\nThe usage is, for example:\n`' + pfx + cmd_wow_character + ' EU Doomhammer Takamatsuku`')
