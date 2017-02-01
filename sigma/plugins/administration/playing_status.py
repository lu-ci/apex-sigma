import discord
from config import Prefix


async def playing_status(ev):
    game_name = Prefix + 'help'
    game = discord.Game(name=game_name)
    await ev.bot.change_presence(game=game)
