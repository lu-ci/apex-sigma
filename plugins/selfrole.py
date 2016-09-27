from plugin import Plugin
from utils import create_logger
from utils import checkPermissions
import asyncio

target_channel = ['roles']
#self_roles = ['Aqua', 'Crimson', 'Red', 'Scarlet', 'CS:GO']
self_roles = ['Grass Green', 'Peach', 'Yellow', 'Light Grey', 'Dark Orange', 'Teal', 'Red', 'Scarlet', 'Blue', 'Brown', 'Aqua', 'Dirt Brown', 'Gold', 'Purple', 'Dark Green', 'Light Brown', 'Mint Green', 'Green', 'Pink', 'Velvet', 'Turquoise', 'Dark Red', 'Violet', 'Magenta/Fuchsia', 'Dark Grey', 'Black', 'Olive', 'Sweet Blue', 'Light Blue', 'Dark Pink', 'Light Orange', 'Dark Brown', 'Burgundy', 'Lavender', 'Orange', 'Moon blue', 'Dark Blue', 'Crimson', 'Light Yellow', 'Periwinkle', 'Lime Green', 'Dark Purple', 'Overwatch', 'Rocket League', 'Blade and Soul', 'Vindictus', 'Dragon Nest', 'League of Legends', 'CS:GO', 'Pokemon Go']
timeout = 5

cmd_addAssingableRole = 'aar'
cmd_removeAssingableRole = 'rar'

class SelfRole(Plugin):
    is_global = True
    log = create_logger('selfrole')

    async def on_message(self, message, pfx):
        if message.server.id == '92827879448002560':
            if message.content.startswith(pfx + 'dumproles'):
                if checkPermissions(message.author):
                    out = '['
                    for role in self_roles:
                        out += "'" + role + "', "
                    out = out[:-2] + ']'
                    await self.client.send_message(message.channel, out)
                else: 'Insufficient permissions'

            if message.content.startswith(pfx + 'listroles'):
                role_list = 'Currently assingable roles: \n'
                for role in self_roles:
                    role_list += '`' + role + '`, '
                await self.client.send_message(message.channel, role_list[:-2])

            if message.content.startswith(pfx + cmd_addAssingableRole):
                if checkPermissions(message.author):
                    added_role = message.content[len(pfx) + len(cmd_addAssingableRole) + 1:]
                    if added_role in self_roles:
                        await self.client.send_message(message.channel, 'Role is already in the list, aborting')
                        return

                    server_roles = []
                    for role in message.server.roles:
                        server_roles.append(role.name)

                    if added_role in server_roles:
                        self_roles.append(added_role)
                        await self.client.send_message(message.channel, 'Role `{}` is added to the list'.format(added_role))
                        return
                    else:
                        await self.client.send_message(message.channel, 'Role `{}` is not found on the server, aborting'.format(added_role))
                        return
                else: 'Insufficient permissions'

            if message.content.startswith(pfx + cmd_removeAssingableRole):
                if checkPermissions(message.author):
                    removed_role = message.content[len(pfx) + len(cmd_addAssingableRole) + 1:]

                    if removed_role in self_roles:
                        self_roles.remove(removed_role)
                        await self.client.send_message(message.channel, 'Role `{}` was removed from the list'.format(removed_role))
                        return
                    else:
                        await self.client.send_message(message.channel, 'Role `{}` is not on the list, aborting'.format(removed_role))
                        return
                else: 'Insufficient permissions'



            if message.channel.name in target_channel: #if message is in the designated channel
                if message.content in self_roles: #if message has the correct keyword
                    user_has_role = False
                    for role in message.author.roles:
                        if role.name == message.content:
                            if role.name in self_roles: #if user has a role
                                user_has_role = True
                                break

                    for role in message.server.roles:
                        if role.name == message.content:
                            if user_has_role:
                                await self.client.remove_roles(message.author, role)
                                response = await self.client.send_message(message.channel, '<@{0}> Role `{1}` removed'.format(message.author.id, role.name))


                                await asyncio.sleep(timeout)
                                await self.client.delete_message(response)
                                await self.client.delete_message(message)


                                return
                            else:
                                await self.client.add_roles(message.author, role)
                                response = await self.client.send_message(message.channel, '<@{0}> Role `{1}` assigned'.format(message.author.id, role.name))


                                await asyncio.sleep(timeout)
                                await self.client.delete_message(response)
                                await self.client.delete_message(message)


                                return