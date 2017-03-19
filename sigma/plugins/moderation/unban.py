from sigma.core.permission import check_ban
import discord


async def unban(cmd, message, args):
    channel = message.channel
    if args:
        user_q = args[0]
        if message.author is not user_q:
            if check_ban(message.author, channel):
                ban_list = await cmd.bot.get_bans(message.server)
                target_user = None
                for user in ban_list:
                    if user.name.lower() == user_q.lower():
                        target_user = user
                        break
                if target_user:
                    await cmd.bot.unban(message.server, target_user)
                    out_content = discord.Embed(type='rich', color=0x66CC66,
                                                title='✅ ' + target_user.name + 'Unbanned.')
                    await cmd.bot.send_message(message.channel, None, embed=out_content)
                else:
                    out_content = discord.Embed(type='rich', color=0xFF9900,
                                                title=':warning: User Not Found In Ban List.')
                    await cmd.bot.send_message(message.channel, None, embed=out_content)
            else:
                out_content = discord.Embed(type='rich', color=0xDB0000,
                                            title=':no_entry: Insufficient Permissions. Ban Permission Required.')
                await cmd.bot.send_message(message.channel, None, embed=out_content)
    else:
        await cmd.bot.send_message(message.channel, cmd.help())
