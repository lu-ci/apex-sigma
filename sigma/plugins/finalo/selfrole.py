import asyncio

from sigma.plugin import Plugin
from sigma.utils import create_logger, checkPermissions


target_channel = ['roles']
# self_roles = ['Aqua', 'Crimson', 'Red', 'Scarlet', 'CS:GO']
self_roles = ['Dragon Nest', 'PvP [DN]', '4v4 [DN]', 'Wipeout [DN]', 'Guild Rumble [DN]', 'Protect [DN]', 'PvE [DN]',
              'Raids [DN]', 'Nests [DN]', 'Dailies [DN]', 'Starlight [DN]',
              'Blade and Soul', 'PvP [BNS]', 'PvE [BNS]',
              'League of Legends', 'NA [LoL]', 'EU [LoL]', 'OCE [LoL]',
              'Vindictus', 'PvP [Vindi]', 'PvE [Vindi]',
              'Overwatch', 'CS:GO',
              'Black Desert Online', 'PvE [BD]', 'PvP [BD]',
              'Revelation Online', 'PvE [Rev]', 'PvP [Rev]',
              'Team Instinct', 'Team Valor', 'Team Mystic', 'Pokémon',
              'Artists', 'Streamers', 'Entertainers', 'Coders', 'Cosplayers',
              'Welcome Party', 'Cake Shop', 'Weebs']
timeout = 5

cmd_addAssingableRole = 'addar'
cmd_removeAssingableRole = 'remar'


class SelfRole(Plugin):
    is_global = True
    log = create_logger('selfrole')

    async def on_message(self, message, pfx):
        if message.channel.id == '222882496113672193':
            if message.content == 'Pokemon':
                message.content = 'Pokémon'
            if message.author.id == self.client.user.id:
                return
            else:
                await self.client.delete_message(message)
            if message.content.startswith(pfx + 'dumproles'):
                if checkPermissions(message.author):
                    out = '['
                    for role in self_roles:
                        out += "'" + role + "', "
                    out = out[:-2] + ']'
                    outmsg = await self.client.send_message(message.channel, out)
                    asyncio.sleep(timeout)
                    await self.client.delete_message(outmsg)
                else:
                    'Insufficient permissions'

            if message.content.startswith(pfx + 'listroles'):
                role_list = 'Currently assingable roles: \n'
                for role in self_roles:
                    role_list += '`' + role + '`, '
                outmsg = await self.client.send_message(message.channel, role_list[:-2])
                asyncio.sleep(5)
                await self.client.delete_message(outmsg)
            if message.content.startswith(pfx + cmd_addAssingableRole):
                if checkPermissions(message.author):
                    added_role = message.content[len(pfx) + len(cmd_addAssingableRole) + 1:]
                    if added_role in self_roles:
                        outmsg = await self.client.send_message(message.channel,
                                                                'Role is already in the list, aborting')
                        asyncio.sleep(timeout)
                        await self.client.delete_message(outmsg)
                        return

                    server_roles = []
                    for role in message.server.roles:
                        server_roles.append(role.name)

                    if added_role in server_roles:
                        self_roles.append(added_role)
                        outmsg = await self.client.send_message(message.channel,
                                                                'Role `{}` is added to the list'.format(added_role))
                        asyncio.sleep(timeout)
                        await self.client.delete_message(outmsg)
                        return
                    else:
                        outmsg = await self.client.send_message(message.channel,
                                                                'Role `{}` is not found on the server, aborting'.format(
                                                                    added_role))
                        asyncio.sleep(timeout)
                        await self.client.delete_message(outmsg)
                        return
                else:
                    'Insufficient permissions'

            if message.content.startswith(pfx + cmd_removeAssingableRole):
                if checkPermissions(message.author):
                    removed_role = message.content[len(pfx) + len(cmd_addAssingableRole) + 1:]

                    if removed_role in self_roles:
                        self_roles.remove(removed_role)
                        outmsg = await self.client.send_message(message.channel,
                                                                'Role `{}` was removed from the list'.format(
                                                                    removed_role))
                        asyncio.sleep(timeout)
                        await self.client.delete_message(outmsg)
                        return
                    else:
                        outmsg = await self.client.send_message(message.channel,
                                                                'Role `{}` is not on the list, aborting'.format(
                                                                    removed_role))
                        asyncio.sleep(timeout)
                        await self.client.delete_message(outmsg)
                        return
                else:
                    'Insufficient permissions'

            if message.channel.name in target_channel:  # if message is in the designated channel
                if message.content in self_roles:  # if message has the correct keyword
                    user_has_role = False
                    for role in message.author.roles:
                        if role.name == message.content:
                            if role.name in self_roles:  # if user has a role
                                user_has_role = True
                                break

                    for role in message.server.roles:
                        if role.name == message.content:
                            if user_has_role:
                                await self.client.remove_roles(message.author, role)
                                response = await self.client.send_message(message.channel,
                                                                          '<@{0}> Role `{1}` removed'.format(
                                                                              message.author.id, role.name))

                                await asyncio.sleep(timeout)
                                await self.client.delete_message(response)

                                return
                            else:
                                await self.client.add_roles(message.author, role)
                                response = await self.client.send_message(message.channel,
                                                                          '<@{0}> Role `{1}` assigned'.format(
                                                                              message.author.id, role.name))

                                await asyncio.sleep(timeout)
                                await self.client.delete_message(response)

                                return
