import discord
import asyncio
from collections import deque
# from config import pfxfix as pfx
from plugin import Plugin
from utils import create_logger
from config import permitted_id, permitted_roles

client = discord.Client()

karaoke = False
karaoke_mod = True
karaoke_channel = 'Karaoke Room'
karaoke_strict = False
karaoke_override = ['Bot', 'Bots', 'Karaoke Staff', 'Karaoke Spotlight', 'Admin', 'BOT', 'Operation Managers', 'Mods',
                    'Coders']
karaoke_queue = deque()
karaoke_deban = False

cmd_handup = 'handup'
cmd_handdown = 'handdown'
cmd_repertoire = 'repertoire'
cmd_takemic = 'takemic'
cmd_dropmic = 'dropmic'
cmd_startkaraoke = 'startkaraoke'
cmd_karaokemode = 'karaokemode'
cmd_strict = 'karaokestrict'
cmd_forceremove = 'remove'


def checkPermissions(user):
    # Checking a list of permitted users
    # if user.id in permitted_id: return True
    for id in permitted_id:
        if id == user.id: return True

    # Checking a list of permitted roles
    for permitted_role in permitted_roles:
        for user_role in user.roles:
            if user_role.name == permitted_role: return True
    # if (user.id) == '125750263687413760': return True
    # for role in user.roles:
    #        if (role.name == 'Admin'): return True

    return False


def boolToStr(input):
    if input:
        return 'True'
    else:
        return 'False'


# @client.event
class VoiceChangeDetection(Plugin):
    is_global = True
    log = create_logger('voice state')

    async def on_voice_state_update(self, before, after):
        global karaoke
        global karaoke_mod
        global karaoke_channel
        global karaoke_strict

        if karaoke_mod:
            if karaoke:
                try:
                    if after.voice.voice_channel.name == karaoke_channel:
                        if karaoke_strict:
                            for role in after.roles:  # iterate through roles of a user
                                if role.name in karaoke_override:
                                    print('Strict, Overriden, Aborting')
                                    return  # if user has an override role
                            if after.voice.mute == False:  # if user is not muted
                                print('Strict, Not Overriden, Muting')
                                await self.client.server_voice_state(after, mute=True)  # otherwise mute the user
                                return

                        else:
                            if after.voice.mute == True:  # if user is muted
                                print('Not Strict, Ummuting')
                                await self.client.server_voice_state(after, mute=False)  # unmute
                                return

                except AttributeError:
                    pass  # catching an exception when user disconnects from voice (switches voice channel to None)

                if (after.voice.voice_channel == None) or (after.voice.voice_channel.name != karaoke_channel):
                    if after.voice.mute == True:  # if he's muted
                        print('Not in karaoke channel, Unmuting')
                        await self.client.server_voice_state(after, mute=False)  # unmute him


# @client.event
class Control(Plugin):
    is_global = True
    log = create_logger('Karaoke Control')

    async def on_message(self, message, pfx):
        global karaoke
        global karaoke_mod
        global karaoke_channel
        global karaoke_strict
        global karaoke_queue
        global karaoke_deban

        async def lookforstrayspotlight():
            for spotlight in message.server.roles:
                if spotlight.name == 'Karaoke Spotlight':
                    for user in message.server.members:  # iterating through server members
                        for role in user.roles:  # through their roles
                            if role == spotlight:  # looking of spotlight roles
                                await client.remove_roles(user, spotlight)  # taking it away =P

        async def assignspotlight(target):
            for role in message.server.roles:
                if role.name == 'Karaoke Spotlight':
                    await client.add_roles(target, role)

        async def enforcestrictmode():
            karaoke_strict = True
            for channel in message.server.channels:  # iterate through server channels
                if channel.name == karaoke_channel:  # find the karaoke channel
                    for user in channel.voice_members:  # iterate through users in the channel
                        if user in karaoke_override:
                            return
                        else:
                            await self.client.server_voice_state(user, mute=True)  # mute them

        async def disablestrictmode():
            karaoke_strict = False
            for channel in message.server.channels:  # iterate through server channels
                if channel.name == karaoke_channel:  # find the karaoke channel
                    for user in channel.voice_members:  # iterate through users in the channel
                        await self.client.server_voice_state(user, mute=False)  # mute them

        async def isuserinvoicechannel(channel, target):
            for channel in message.server.channels:  # iterate through server channels
                if channel.name == channel:  # find the karaoke channel
                    for user in channel.voice_members:  # iterate through users in the channel
                        if user.id == target:  # user is in the channel
                            return True

        if message.content.startswith(pfx + cmd_karaokemode):
            if checkPermissions(message.author):
                if karaoke_mod:
                    karaoke_mod = False
                    await self.client.send_message(message.channel, "Karaoke mode is set to false, not muting users")
                else:
                    karaoke_mod = True
                    await self.client.send_message(message.channel, "Karaoke mode is set to true, muting users")
            else:
                await self.client.send_message(message.channel, "Insufficient permissions")

        elif message.content.startswith(pfx + cmd_startkaraoke):
            if checkPermissions(message.author):
                target = message.content[len(pfx) + len(cmd_startkaraoke) + 1:]
                if (len(target)) == 0:
                    await self.client.send_message(message.channel, "No channel specified, aborting")
                    return

                global karaoke, karaoke_channel, karaoke_strict
                karaoke = True
                karaoke_channel = target
                karaoke_strict = True
                try:
                    for channel in message.server.channels:  # iterate through server channels
                        if channel.name == karaoke_channel:  # find the karaoke channel
                            for user in channel.voice_members:  # iterate through users in the channel
                                for role in user.roles:
                                    if role.name in karaoke_override:  # if user has an override role
                                        break
                                else:
                                    await self.client.server_voice_state(user, mute=True)  # mute them
                    await self.client.send_message(message.channel,
                                                   "Karaoke started in strict mode on channel " + karaoke_channel)
                except SyntaxError:
                    await self.client.send_message(message.channel, "Error while starting karaoke session")
            else:
                await self.client.send_message(message.channel, "Insufficient permissions")

        elif message.content.startswith(pfx + 'stopkaraoke'):
            if checkPermissions(message.author):

                if karaoke:
                    karaoke = False
                    for channel in message.server.channels:  # iterate through server channels
                        if channel.name == karaoke_channel:  # find the karaoke channel
                            for user in channel.voice_members:  # iterate through users in the channel
                                await self.client.server_voice_state(user, mute=False)  # unmute them
                    await self.client.send_message(message.channel, "Karaoke stopped")
                else:
                    await self.client.send_message(message.channel, "No ongoing karaoke found")
            else:
                await self.client.send_message(message.channel, "Insufficient permissions")

        elif message.content.startswith(pfx + cmd_strict):
            if checkPermissions(message.author):

                if karaoke_strict:
                    karaoke_strict = False
                    for channel in message.server.channels:  # iterate through server channels
                        if channel.name == karaoke_channel:  # find the karaoke channel
                            for user in channel.voice_members:  # iterate through users in the channel
                                await self.client.server_voice_state(user, mute=False)  # unmute them
                    await self.client.send_message(message.channel, "Strict mode disabled")
                else:
                    karaoke_strict = True
                    for channel in message.server.channels:  # iterate through server channels
                        if channel.name == karaoke_channel:  # find the karaoke channel
                            for user in channel.voice_members:  # iterate through users in the channel
                                for role in user.roles:  # iterate through roles of a user
                                    if role in karaoke_override:
                                        return
                                    else:
                                        await self.client.server_voice_state(user, mute=True)  # mute them
                    await self.client.send_message(message.channel, "Strict mode enabled")
            else:
                await self.client.send_message(message.channel, "Insufficient permissions")

        elif message.content.startswith(pfx + cmd_handup):
            await self.client.send_typing(message.channel)
            if karaoke:
                if not message.author.id in karaoke_queue:
                    karaoke_queue.append(message.author.id)
                    await self.client.send_message(message.channel,
                                                   '<@' + message.author.id + '> has joined the singers list!\nA round of applause please! :musical_note: :clap:')
                else:
                    await self.client.send_message(message.channel,
                                                   'I\'m sorry <@' + message.author.id + '>, but you\'re already on the list...')
            else:
                await self.client.send_message(message.channel, 'No karaoke session running')

        elif message.content.startswith(pfx + cmd_repertoire):
            if karaoke:
                await self.client.send_typing(message.channel)
                if len(karaoke_queue) != 0:
                    singer_list = ''
                    n = 1
                    for user in karaoke_queue:
                        singer_list += '\n#' + str(n) + ': <@' + str(user) + '>'
                        n += 1
                    await self.client.send_message(message.channel, singer_list)
                else:
                    await self.client.send_message(message.channel, 'The list seems to be empty')
            else:
                await self.client.send_message(message.channel, 'No karaoke session running')

        elif message.content.startswith(pfx + 'clearqueue'):
            if checkPermissions(message.author):
                karaoke_queue.clear()
                await self.client.send_message(message.channel, 'Karaoke queue cleared')

        elif message.content.startswith(pfx + cmd_forceremove):
            if checkPermissions(message.author):
                target = message.content[len(pfx) + len(cmd_forceremove) + 1:]
                if (len(target)) == 0:
                    await self.client.send_message(message.channel, "No user specified, aborting")
                    return
                if message.mentions[0].id in karaoke_queue:
                    karaoke_queue.remove(message.mentions[0].id)
                    await self.client.send_message(message.channel, 'User removed from the queue')
                else:
                    await self.client.send_message(message.channel, 'User not found in the queue')

        elif message.content.startswith(pfx + cmd_handdown):
            if karaoke:
                if message.author.id in karaoke_queue:
                    karaoke_queue.remove(message.author.id)
                    await self.client.send_message(message.channel,
                                                   'You have been removed from the list!\nWe\'re sorry to see you go, <@' + message.author.id + '>... :cry:')
                else:
                    await self.client.send_message(message.channel, 'I can\'t find you on the list...')
            else:
                await self.client.send_message(message.channel, 'No karaoke session running')

        elif message.content.startswith(pfx + cmd_takemic):
            if not karaoke_deban:  # if its not someone's else turn
                if message.author.id in karaoke_queue:  # if user is in the queue
                    if message.author.id == karaoke_queue[0]:  # if its his/her turn
                        if isuserinvoicechannel(karaoke_channel, karaoke_queue[0]):
                            karaoke_deban = [True, karaoke_queue.popleft()]

                            await lookforstrayspotlight()
                            await assignspotlight(karaoke_deban[1])
                            await self.client.send_message(message.channel,
                                                           '<@' + karaoke_deban[
                                                               1] + '> is morally ready, enforcing strict mode')
                            await enforcestrictmode()

                        else:
                            self.client.send_message(message.channel,
                                                     '<@' + karaoke_queue[0] + "> you're not in karaoke channel")
                    else:
                        await self.client.send_message(message.channel,
                                                       "<@" + message.author.id + "> it's not your turn yet")
                else:
                    await self.client.send_message(message.channel,
                                                   "<@" + message.author.id + "> you're not in the queue")
            else:
                self.client.send_message(message.channel, "Shh, it's <@" + karaoke_deban[1] + "> singing time")

        elif message.content.startswith(pfx + cmd_dropmic):
            print(karaoke_deban)
            try:
                if karaoke_deban[0]:
                    if message.author.id == karaoke_deban[1]:
                        karaoke_strict = False
                        for channel in message.server.channels:  # iterate through server channels
                            if channel.name == karaoke_channel:  # find the karaoke channel
                                for user in channel.voice_members:
                                    await self.client.server_voice_state(user, mute=False)  # unmute them
                        await self.client.send_message(message.channel,
                                                       'こら! <@' + karaoke_deban[1] + '>! That breaks the mic!')
                        karaoke_deban = [False, 0]
                else:
                    await self.client.send_message(message.channel,
                                                   "What do you think you're dropping <@" + message.author.id + "> ?")
            except TypeError:
                await self.client.send_message(message.channel,
                                               "What do you think you're dropping <@" + message.author.id + "> ?")


        elif message.content.startswith(pfx + 'status'):
            out = 'Karaoke mode ' + boolToStr(karaoke_mod) + '\n'
            out += 'Session ongoing ' + boolToStr(karaoke) + '\n'
            out += 'Channel ' + karaoke_channel + '\n'
            out += 'Strict mode ' + boolToStr(karaoke_strict)

            await self.client.send_message(message.channel, out)

        elif message.content.startswith(pfx + 'test1'):
            print('test1')
            await lookforstrayspotlight()
            # for spotlight in message.server.roles:
            #    if spotlight.name == 'Karaoke Spotlight':
            #        for user in message.server.members:
            #            for role in user.roles:
            #                if role == spotlight:
            #                    await client.remove_roles(user, spotlight)

        elif message.content.startswith(pfx + 'test2'):
            print('test2')
            for role in message.server.roles:
                if role.name == 'Karaoke Spotlight':
                    await client.add_roles(message.author, role)
                    return

        elif message.content.startswith(pfx + 'test3'):
            print('test2')
            for role in message.server.roles:
                if role.name == 'Karaoke Spotlight':
                    await client.remove_roles(message.author, role)
                    return



                    # elif message.content.startswith(pfx + 'karaokestrict'):
                    #   if karaoke_strict:
                    #       karaoke_strict = False
                    #       for channel in message.server.channels: #iterate through server channels
                    #           if channel.name == karaoke_channel: #find the karaoke channel
                    #               for user in channel.voice_members: #iterate through users in the channel
                    #                   await self.client.server_voice_state(user, mute=False) #unmute them
                    #       await self.client.send_message(message.channel, "Strict mode disabled")
                    #   else:
                    #       karaoke_strict = True
                    #       for channel in message.server.channels: #iterate through server channels
                    #           if channel.name == karaoke_channel: #find the karaoke channel
                    #               for user in channel.voice_members: #iterate through users in the channel
                    #                   await self.client.server_voice_state(user, mute=True) #mute them
                    #       await self.client.send_message(message.channel, "Strict mode enabled")

                    # elif message.content.startswith(pfx + 'karaoke'):
                    #    await self.client.send_typing(message.channel)
                    #    cmd_name = 'Repertiore'
                    #    dbsql = sqlite3.connect('storage/server_settings.sqlite', timeout=20)
                    #    #self.log.info('\nUser %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                    #    #              message.author,
                    #    #              message.author.id, message.server.name, message.server.id, message.channel)
                    #    await self.client.send_message(message.channel,
                    #                                   '```css\n[' + pfx + cmd_handup + '] Adds you to the singers list.' +
                    #                                   '\n[' + pfx + cmd_handdown + '] Removes you to the singers list.' +
                    #                                   '\n[' + pfx + cmd_repertoire + '] Lists the current singers.' +
                    #                                   '\n[' + pfx + cmd_takemic + '] Mutes everyone except you so you can start.' +
                    #                                   '\n[' + pfx + cmd_dropmic + '] Unmutes everyone and marks your performance as done.' +
                    #                                   '\n[' + pfx + 'karaoke' + '] Lists these commands.' +
                    #                                   '\n```')
