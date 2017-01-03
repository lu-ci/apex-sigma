import asyncio
import discord

from config import permitted_id


async def setgame(cmd, message, args):
    if message.author.id in permitted_id:
        gamename = ' '.join(args)

        game = discord.Game(name=gamename)
        await cmd.bot.change_presence(game=game)

        embed = discord.Embed(title=':white_check_mark: Now Playing Set', color=0x66CC66)
        response = await cmd.bot.send_message(message.channel, None, embed=embed)
        await asyncio.sleep(5)
        await cmd.bot.delete_message(response)
    else:
        out = discord.Embed(type='rich', color=0xDB0000,
                            title=':no_entry: Insufficient Permissions. Bot Owner Only.')
        response = await cmd.bot.send_message(message.channel, None, embed=out)
        await asyncio.sleep(5)
        await cmd.bot.delete_message(response)
