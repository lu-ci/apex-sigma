import discord
from collections import deque

from sigma.plugin import Plugin
from sigma.utils import create_logger, bold

from config import permitted_id, permitted_roles
from config import permitted_roles as karaoke_override


client = discord.Client()

karaoke = False
karaoke_mod = True
karaoke_channel = 'Music Room'
karaoke_strict = False

karaoke_queue = deque()
karaoke_deban = [False, 0]


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
        log = True
        if karaoke_mod:
            if karaoke:
                # print("karaoke's running")
                if (after.voice.voice_channel == None) or (after.voice.voice_channel.name != karaoke_channel):
                    if after.voice.mute == True:  # if he's muted
                        if log: print('not in karaoke channel, unmuting')
                        await self.client.server_voice_state(after, mute=False)  # unmute him
                try:
                    if after.voice.voice_channel.name == karaoke_channel:
                        if karaoke_strict:
                            for role in after.roles:  # iterate through roles of a user
                                if role.name in karaoke_override:
                                    if log: print('strict, overriden, aborting')
                                    return  # if user has an override role
                            if after.voice.mute == False:  # if user is not muted
                                if log: print('strict, not overriden, muting')
                                await self.client.server_voice_state(after, mute=True)  # otherwise mute the user
                                return

                        else:
                            if after.voice.mute == True:  # if user is muted
                                if log: print('not strict, ummuting')
                                await self.client.server_voice_state(after, mute=False)  # unmute
                                return

                except AttributeError:
                    pass  # catching an exception when user disconnects from voice (switches voice channel to None)

                if (after.voice.voice_channel == None) or (after.voice.voice_channel.name != karaoke_channel):
                    if after.voice.mute == True:  # if he's muted
                        if log: print('not in karaoke channel, unmuting')
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

        async def lookforstrayspotlight(server):
            for spotlight in server.roles:
                if spotlight.name == 'Karaoke Spotlight':
                    for user in server.members:  # iterating through server members
                        for role in user.roles:  # through their roles
                            if role == spotlight:  # looking of spotlight roles
                                await self.client.remove_roles(user, spotlight)  # taking it away =P

        async def assignspotlight(target):
            for role in target.server.roles:
                if role.name == 'Karaoke Spotlight':
                    await self.client.add_roles(target, role)

        async def enforcestrictmode():
            global karaoke_strict
            karaoke_strict = True
            temp = []
            for channel in message.server.channels:  # iterate through server channels
                if channel.name == karaoke_channel:  # find the karaoke channel
                    for user in channel.voice_members:  # iterate through users in the channel
                        temp.append(user)

            for user in temp:
                overridden = False
                for role in user.roles:
                    if role.name in karaoke_override:
                        overridden = True
                        break
                if not overridden:
                    await self.client.server_voice_state(user, mute=True)
                    # else: await self.client.server_voice_state(user, mute = True)
                    # for channel in message.server.channels:  # iterate through server channels
                    #    if channel.name == karaoke_channel:  # find the karaoke channel
                    #        for user in channel.voice_members:  # iterate through users in the channel
                    #            if user in karaoke_override:
                    #                return
                    #            else:
                    #                await self.client.server_voice_state(user, mute=True)  # mute them

        async def disablestrictmode():
            for channel in message.server.channels:  # iterate through server channels
                if channel.name == karaoke_channel:  # find the karaoke channel
                    for user in channel.voice_members:  # iterate through users in the channel
                        await self.client.server_voice_state(user, mute=False)  # mute them

        async def isuserinvoicechannel(target_channel, target_user):
            for channel in message.server.channels:  # iterate through server channels
                if channel.name == target_channel:  # find the karaoke channel
                    for user in channel.voice_members:  # iterate through users in the channel
                        if user.id == target_user.id:  # user is in the channel
                            return True
            return False

        async def mutekaraokechannel():
            temp = []
            for channel in message.server.channels:  # iterate through server channels
                if channel.name == karaoke_channel:  # find the karaoke channel
                    for user in channel.voice_members:  # iterate through users in the channel
                        temp.append(user)
            for user in temp:
                await self.client.server_voice_state(user, mute=True)  # unmute them

        async def unmutekaraokechannel():
            temp = []
            for channel in message.server.channels:  # iterate through server channels
                if channel.name == karaoke_channel:  # find the karaoke channel
                    for user in channel.voice_members:  # iterate through users in the channel
                        temp.append(user)
            for user in temp:
                await self.client.server_voice_state(user, mute=False)  # unmute them
