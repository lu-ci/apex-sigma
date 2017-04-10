from config import permitted_id
import discord

async def echo(cmd, message, args):
    if message.author.id in permitted_id:
        await message.channel.send(' '.join(args))
    else:
        status = discord.Embed(type='rich', color=0xDB0000,
                               title='⛔ Insufficient Permissions. Bot Owner Only.')
        await message.channel.send(None, embed=status)
