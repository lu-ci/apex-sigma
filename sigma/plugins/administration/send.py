import asyncio
import discord
from config import permitted_id


async def send(cmd, message, args):
    if message.author.id in permitted_id:
        if not args:
            await cmd.bot.send_message(message.channel, cmd.help())
            return
        else:
            if len(args) < 2:
                await cmd.bot.send_message(message.channel, cmd.help())
                return
            else:
                try:
                    server = None
                    locator_content = args[0]
                    text_content = ' '.join(args[1:])
                    split_locator = locator_content.split('|')
                    server_search = split_locator[0]
                    varies = split_locator[1]
                    varies_split = varies.split(':')
                    mode = varies_split[0].lower()
                    if mode not in ['c', 'u']:
                        await cmd.bot.send_message(message.channel, cmd.help())
                        return
                    target_id = varies_split[1]
                    found_server = 0
                    found_channel = 0
                    found_user = 0
                    for server in cmd.bot.servers:
                        if server.id == server_search:
                            found_server += 1
                            if mode == 'c':
                                for channel in server.channels:
                                    if channel.id == target_id:
                                        found_channel += 1
                                        await cmd.bot.send_message(channel, text_content)
                                        embed = discord.Embed(title=':information_source: Message Sent', color=0x0099FF)
                                        embed.add_field(name='Server', value=server.name)
                                        embed.add_field(name='Channel', value='#' + channel.name)
                                        await cmd.bot.send_message(message.channel, None, embed=embed)
                                        break
                            elif mode == 'u':
                                for user in server.members:
                                    if user.id == target_id:
                                        found_user += 1
                                        await cmd.bot.start_private_message(user=user)
                                        await cmd.bot.send_message(user, text_content)
                                        embed = discord.Embed(title=':information_source: Message Sent', color=0x0099FF)
                                        embed.add_field(name='Server', value=server.name)
                                        embed.add_field(name='User', value=user.name + '#' + user.discriminator)
                                        await cmd.bot.send_message(message.channel, None, embed=embed)
                                        break
                            else:
                                embed = discord.Embed(title=':exclamation: Error', color=0xDB0000)
                                embed.add_field(name='Invalid Mode',
                                                value='Use either **C** for Channel or **U** for User.')
                                await cmd.bot.send_message(message.channel, None, embed=embed)
                    if found_server == 0:
                        embed = discord.Embed(title=':exclamation: No server with that ID found.', color=0xDB0000)
                        await cmd.bot.send_message(message.channel, None, embed=embed)
                        return
                    else:
                        if mode == 'c':
                            if found_channel == 0:
                                embed = discord.Embed(
                                    title=':exclamation: No channel with that ID was found on ' + server.name + '.',
                                    color=0xDB0000)
                                await cmd.bot.send_message(message.channel, None, embed=embed)
                        if mode == 'u':
                            if found_user == 0:
                                embed = discord.Embed(
                                    title=':exclamation: No user with that ID was found on ' + server.name + '.',
                                    color=0xDB0000)
                                await cmd.bot.send_message(message.channel, None, embed=embed)
                except Exception as e:
                    cmd.log.error(e)
                    embed = discord.Embed(color=0xDB0000)
                    embed.add_field(name=':exclamation: Error', value=str(e))
                    await cmd.bot.send_message(message.channel, None, embed=embed)
                    return
    else:
        out = discord.Embed(type='rich', color=0xDB0000,
                            title=':no_entry: Insufficient Permissions. Bot Owner Only.')
        await cmd.bot.send_message(message.channel, None, embed=out)
