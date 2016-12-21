from sigma.core.permission import check_ban
import discord


async def ban(cmd, message, args):
    channel = message.channel
    if message.mentions:
        user_q = message.mentions[0]
        if message.author is not user_q:
            if check_ban(message.author, channel):
                try:
                    await cmd.bot.ban(user_q)
                    out_content = discord.Embed(color=0x0099FF,
                                                title=':information_source: User **' + user_q.name + '** has been banned.')
                    await cmd.bot.send_message(message.channel, None, embed=out_content)
                    await cmd.bot.send_message(message.channel, )
                except Exception as e:
                    cmd.log.error(e)
                    await cmd.bot.send_message(message.channel, str(e))
            else:
                out_content = discord.Embed(color=0xDB0000,
                                            title=':no_entry: Insufficient Permissions. Users with Ban permissions only.')
                await cmd.bot.send_message(message.channel, None, embed=out_content)
        else:
            await cmd.bot.send_message(message.channel, cmd.help())
    else:
        await cmd.bot.send_message(message.channel, cmd.help())
