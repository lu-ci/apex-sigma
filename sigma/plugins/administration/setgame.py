import asyncio
import discord


async def setgame(cmd, message, args):
    gamename = ' '.join(args)

    game = discord.Game(name=gamename)
    await cmd.bot.change_presence(game=game)

    embed = discord.Embed(title='✅ Now Playing Set', color=0x66CC66)
    response = await message.channel.send(None, embed=embed)
    await asyncio.sleep(5)
    await response.delete()
