import secrets
import discord


async def choose(cmd, message, args):
    if args:
        choice = secrets.choice(' '.join(args).split('; '))
        embed = discord.Embed(color=0x1ABC9C, title=':thinking: I choose... ' + choice)
        await message.channel.send(None, embed=embed)
    else:
        await message.channel.send(cmd.help())
        return
