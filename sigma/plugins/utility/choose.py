import random
import discord


async def choose(cmd, message, args):
    if args:
        choice = random.choice(args)
        embed = discord.Embed(color=0x1ABC9C, title=':thinking: I choose... ' + choice)
        await cmd.bot.send_message(message.channel, None, embed=embed)
    else:
        await cmd.bot.send_message(message.channel, cmd.help())
        return
