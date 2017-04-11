import discord


async def setname(cmd, message, args):
    if args:
        username = ' '.join(args)
        await cmd.bot.user.edit(name=username)
        embed = discord.Embed(title='✅ Changed Username', color=0x66CC66)
        await message.channel.send(None, embed=embed)
