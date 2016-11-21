import asyncio
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
                                        await cmd.bot.send_message(message.channel,
                                                                   'Message has been sent to **' + channel.name + '** on **' + server.name + '**.')
                                        break
                            elif mode == 'u':
                                for user in server.members:
                                    if user.id == target_id:
                                        found_user += 1
                                        await cmd.bot.start_private_message(user=user)
                                        await cmd.bot.send_message(user, text_content)
                                        await cmd.bot.send_message(message.channel,
                                                                   'Message has been sent to **' + user.name + '** on **' + server.name + '**.')
                                        break
                            else:
                                await cmd.bot.send_message(message.channel,
                                                           'Invalid mode.\nUse either `c` for channel, or `u` for user.')
                    if found_server == 0:
                        await cmd.bot.send_message(message.channel, 'No server by that ID was found.')
                        return
                    else:
                        if mode == 'c':
                            if found_channel == 0:
                                await cmd.bot.send_message(message.channel, 'No channel by that ID was found on.')
                        if mode == 'u':
                            if found_user == 0:
                                await cmd.bot.send_message(message.channel, 'No user by that ID was found.')

                except Exception as e:
                    cmd.log.error(e)
                    await cmd.bot.send_message(message.channel, str(e))
                    return
    else:
        response = await cmd.bot.send_message(message.channel, 'Insufficient permissions. :x:')
        await asyncio.sleep(10)
        await cmd.bot.delete_message(response)
