import requests

from sigma.plugin import Plugin
from sigma.utils import create_logger

from config import BlizzardKey


class World_Of_Warcraft(Plugin):
    is_global = True
    log = create_logger('wow')

    async def on_message(self, message, pfx):
        if message.content.startswith(pfx + 'wowchar' + ' '):
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
            query = message.content[len(pfx) + len('wowchar') + 1:].replace('_', '%20')
            try:
                region_raw, realm, char_name = query.split(maxsplit=2)
            except:
                await self.client.send_message(message.channel,
                                               'Invalid Input Format, please reffer to the example:\n`' + pfx + 'wowchar' + ' EU Doomhammer Takamatsuku`')
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

                out_data = ''
                out_data += '\nName: \"' + char_ig_name + '\"'
                out_data += '\nRealm: \"' + char_realm + '\"'
                out_data += '\nLevel: \"' + str(char_level) + '\"'
                out_data += '\nRace: \"' + race_name + '\"'
                out_data += '\nClass: \"' + class_name + '\"'
                out_data += '\nGender: \"' + gender_name + '\"'
                out_data += '\nName: \"' + char_ig_name + '\"'
                out_data += '\nBattlegroup: \"' + battlegroup + '\"'
                out_data += '\nAchievement Points: \"' + str(char_achi_points) + '\"'
                out_data += '\nHonorable Kills: \"' + str(hon_kills) + '\"'
                out_data += '\nThumbnail: \"' + image_url + '\"'

                out_eqp = ''
                out_eqp += '\nAverage Equipment Level: \"' + str(avg_item_level) + '\"'
                out_eqp += '\nHead: \"' + item_head + '\"'
                out_eqp += '\nNeck: \"' + item_neck + '\"'
                out_eqp += '\nShoulder: \"' + item_shoulder + '\"'
                out_eqp += '\nBack: \"' + item_back + '\"'
                out_eqp += '\nChest: \"' + item_chest + '\"'
                out_eqp += '\nShirt: \"' + item_shirt + '\"'
                out_eqp += '\nTabard: \"' + item_tabard + '\"'
                out_eqp += '\nWrist: \"' + item_wrist + '\"'
                out_eqp += '\nHands: \"' + item_hands + '\"'
                out_eqp += '\nWaist: \"' + item_waist + '\"'
                out_eqp += '\nLegs: \"' + item_legs + '\"'
                out_eqp += '\nFeet: \"' + item_feet + '\"'
                out_eqp += '\nFinger 1: \"' + item_finger1 + '\"'
                out_eqp += '\nFinger 2: \"' + item_finger2 + '\"'
                out_eqp += '\nTrinket 1: \"' + item_trinket1 + '\"'
                out_eqp += '\nTrinket 2: \"' + item_trinket2 + '\"'
                out_eqp += '\nMain Hand: \"' + item_main_hand + '\"'
                out_eqp += '\nOff Hand: \"' + item_off_hand + '\"'

                await self.client.send_message(message.channel,
                                               ':ticket: Basic Stats:\n```python\n' + out_data + '\n```')
                await self.client.send_message(message.channel, ':shirt: Equipment:\n```python\n' + out_eqp + '\n```')
            except:
                try:
                    error_no = char_data['status']
                    error_msg = char_data['reason']
                    await self.client.send_message(message.channel, 'Error: ' + str(error_no) + '\n' + error_msg)
                except:
                    await self.client.send_message(message.channel,
                                                   'Something went wrong, most likely invalid region...\nRegions are: `US`, `EU`, `KR`, `TW`\nThe usage is, for example:\n`' + pfx + 'wowchar' + ' EU Doomhammer Takamatsuku`')
