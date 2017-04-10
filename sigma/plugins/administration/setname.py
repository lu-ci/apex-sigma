import discord


async def setname(cmd, message, args):
    if not args:
        await message.channel.send(cmd.help())
        return
    else:
        username = ' '.join(args)
        await cmd.bot.edit_profile(username=username)
        embed = discord.Embed(title='✅ Changed Username', color=0x66CC66)
        await message.channel.send(None, embed=embed)
