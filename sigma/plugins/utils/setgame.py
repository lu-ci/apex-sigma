import asyncio
import discord

from config import permitted_id


async def setgame(cmd, message, args):
    if message.author.id in permitted_id:
        gamename = ' '.join(args)

        game = discord.Game(name=gamename)
        await cmd.bot.change_presence(game=game)

        response = await cmd.reply('Done! :ok_hand:')
        await asyncio.sleep(5)
        await cmd.bot.delete_message(response)
    else:
        response = await cmd.reply('Insufficient permissions...')
        await asyncio.sleep(5)
        await cmd.bot.delete_message(response)
