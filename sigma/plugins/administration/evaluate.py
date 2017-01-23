from config import permitted_id
import discord
import random
import os
import lxml
import asyncio
import codecs


async def evaluate(cmd, message, args):
    if message.author.id in permitted_id:
        if not args:
            await cmd.bot.send_message(message.channel, cmd.help())
        else:
            try:
                execution = " ".join(args)
                output = eval(execution)
                status = discord.Embed(title=':white_check_mark: Executed', color=0x66CC66)
                if output:
                    try:
                        status.add_field(name='Results', value='\n```\n' + str(output) + '\n```')
                    except:
                        pass
            except Exception as e:
                cmd.log.error(e)
                status = discord.Embed(type='rich', color=0xDB0000,
                                       title=':exclamation: Error')
                status.add_field(name='Execution Failed', value=str(e))
            await cmd.bot.send_message(message.channel, None, embed=status)
    else:
        status = discord.Embed(type='rich', color=0xDB0000,
                               title=':no_entry: Insufficient Permissions. Bot Owner or Server Admin Only.')
        await cmd.bot.send_message(message.channel, None, embed=status)
