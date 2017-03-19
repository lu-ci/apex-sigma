from sigma.core.permission import check_ban
import discord


async def ban(cmd, message, args):
    channel = message.channel
    if message.mentions:
        user_q = message.mentions[0]
        if message.author is not user_q:
            if check_ban(message.author, channel):
                await cmd.bot.ban(user_q)
                out_content = discord.Embed(color=0xFF9900,
                                            title=':hammer: User **' + user_q.name + '** has been banned!')
                await cmd.bot.send_message(message.channel, None, embed=out_content)
            else:
                out_content = discord.Embed(color=0xDB0000,
                                            title='⛔ Insufficient Permissions. Users with Ban permissions only.')
                await cmd.bot.send_message(message.channel, None, embed=out_content)
        else:
            await cmd.bot.send_message(message.channel, cmd.help())
    else:
        await cmd.bot.send_message(message.channel, cmd.help())
