from sigma.core.permission import check_ban
import discord


async def softban(cmd, message, args):
    channel = message.channel
    if args[0]:
        user_q = message.mentions[0]
        if message.author is not user_q:
            if check_ban(message.author, channel):
                try:
                    await cmd.bot.ban(user_q)
                    await cmd.bot.unban(message.server, user_q)
                    embed = discord.Embed(color=0x66CC66,
                                          title=':white_check_mark: ' + user_q.name + ' has been soft-banned.')
                    await cmd.bot.send_message(message.channel, None, embed=embed)
                except Exception as e:
                    cmd.log.error(e)
                    await cmd.bot.send_message(message.channel, str(e))
            else:
                out_content = discord.Embed(type='rich', color=0xDB0000,
                                            title=':no_entry: Insufficient Permissions. Ban Permission Required.')
                await cmd.bot.send_message(message.channel, None, embed=out_content)
