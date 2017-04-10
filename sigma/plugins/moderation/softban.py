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
                    await cmd.bot.unban(message.guild, user_q)
                    embed = discord.Embed(color=0x66CC66,
                                          title='✅ ' + user_q.name + ' has been soft-banned.')
                    await message.channel.send(None, embed=embed)
                except Exception as e:
                    cmd.log.error(e)
                    await message.channel.send(str(e))
            else:
                out_content = discord.Embed(type='rich', color=0xDB0000,
                                            title='⛔ Insufficient Permissions. Ban Permission Required.')
                await message.channel.send(None, embed=out_content)
