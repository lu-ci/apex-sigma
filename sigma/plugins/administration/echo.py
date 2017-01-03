from config import permitted_id
import discord

async def echo(cmd, message, args):
    if message.author.id in permitted_id:
        await cmd.bot.send_message(message.channel, ' '.join(args))
    else:
        status = discord.Embed(type='rich', color=0xDB0000,
                               title=':no_entry: Insufficient Permissions. Bot Owner Only.')
        await cmd.bot.send_message(message.channel, None, embed=status)
