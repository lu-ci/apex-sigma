import discord
from sigma.core.permission import check_kick


async def warnlimit(cmd, message, args):
    if not check_kick(message.author, message.channel):
        out_content = discord.Embed(color=0xDB0000,
                                    title='⛔ Server Admin Only.')
        await message.channel.send(None, embed=out_content)
        return
    if not args:
        try:
            warn_limit = cmd.db.get_settings(message.guild.id, 'WarnLimit')
        except KeyError:
            cmd.db.set_settings(message.guild.id, 'WarnLimit', 2)
            warn_limit = 2
        out_content = discord.Embed(color=0x0099FF, title='ℹ Current Warning Limit Is ' + str(warn_limit))
        await message.channel.send(None, embed=out_content)
    else:
        try:
            new_limit = abs(int(args[0]))
        except:
            out_content = discord.Embed(color=0xDB0000, title='❗ Invalid Number')
            await message.channel.send(None, embed=out_content)
            return
        cmd.db.set_settings(message.guild.id, 'WarnLimit', new_limit)
        out_content = discord.Embed(color=0x0099FF, title='ℹ New Limit Set To ' + str(new_limit))
        await message.channel.send(None, embed=out_content)
