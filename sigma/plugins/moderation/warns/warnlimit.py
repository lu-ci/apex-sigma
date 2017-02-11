import discord
from sigma.core.permission import check_kick


async def warnlimit(cmd, message, args):
    if not check_kick(message.author, message.channel):
        out_content = discord.Embed(color=0xDB0000,
                                    title=':no_entry: Server Admin Only.')
        await cmd.bot.send_message(message.channel, None, embed=out_content)
        return
    if not args:
        try:
            warn_limit = cmd.db.get_settings(message.server.id, 'WarnLimit')
        except KeyError:
            cmd.db.set_settings(message.server.id, 'WarnLimit', 2)
            warn_limit = 2
        out_content = discord.Embed(color=0x0099FF, title='ℹ Current Warning Limit Is ' + str(warn_limit))
        await cmd.bot.send_message(message.channel, None, embed=out_content)
    else:
        try:
            new_limit = abs(int(args[0]))
        except:
            out_content = discord.Embed(color=0xDB0000, title=':exclamation: Invalid Number')
            await cmd.bot.send_message(message.channel, None, embed=out_content)
            return
        cmd.db.set_settings(message.server.id, 'WarnLimit', new_limit)
        out_content = discord.Embed(color=0x0099FF, title='ℹ New Limit Set To ' + str(new_limit))
        await cmd.bot.send_message(message.channel, None, embed=out_content)
