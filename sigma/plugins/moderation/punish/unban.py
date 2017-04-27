from sigma.core.permission import check_ban
import discord


async def unban(cmd, message, args):
    channel = message.channel
    if args:
        user_q = args[0]
        if message.author is not user_q:
            if check_ban(message.author, channel):
                ban_list = await message.guild.bans()
                target_user = None
                for user in ban_list:
                    if user.name.lower() == user_q.lower():
                        target_user = user
                        break
                if target_user:
                    await cmd.bot.unban(message.guild, target_user)
                    out_content = discord.Embed(type='rich', color=0x66CC66,
                                                title='✅ ' + target_user.name + 'Unbanned.')
                    await message.channel.send(None, embed=out_content)
                else:
                    out_content = discord.Embed(type='rich', color=0xFF9900,
                                                title='⚠ User Not Found In Ban List.')
                    await message.channel.send(None, embed=out_content)
            else:
                out_content = discord.Embed(type='rich', color=0xDB0000,
                                            title='⛔ Insufficient Permissions. Ban Permission Required.')
                await message.channel.send(None, embed=out_content)
    else:
        await message.channel.send(cmd.help())
