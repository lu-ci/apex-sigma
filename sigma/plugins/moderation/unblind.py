from sigma.core.permission import check_man_msg
from sigma.core.permission import check_man_roles
from sigma.core.permission import check_write
import discord


async def unblind(cmd, message, args):
    channel = message.channel
    server = message.server
    if not message.mentions:
        await cmd.bot.send_message(message.channel, cmd.help())
        return
    user_q = message.mentions[0]
    if message.author is not user_q:
        if check_man_msg(message.author, channel) and check_man_roles(message.author, channel):
            for chan in server.channels:
                if str(chan.type).lower() == 'text':
                    if not check_write(user_q, chan):
                        await cmd.bot.delete_channel_permissions(chan, user_q)
            embed = discord.Embed(color=0x66CC66, title='✅ ' + user_q.name + ' can see again.')
            await cmd.bot.send_message(message.channel, None, embed=embed)
        else:
            out_content = discord.Embed(type='rich', color=0xDB0000,
                                        title='⛔ Insufficient Permissions. Manage Messages and Manage Roles Permissions Required.')
            await cmd.bot.send_message(message.channel, None, embed=out_content)
