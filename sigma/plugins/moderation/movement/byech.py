import discord
from sigma.core.permission import check_admin


async def byech(cmd, message, args):
    if not check_admin(message.author, message.channel):
        embed = discord.Embed(title='⛔ Unpermitted. Server Admin Only.', color=0xDB0000)
    else:
        if message.channel_mentions:
            target_channel = message.channel_mentions[0]
        else:
            target_channel = message.channel
        cmd.db.set_settings(message.guild.id, 'ByeChannel', target_channel.id)
        embed = discord.Embed(color=0x66CC66, title=f'✅ Goodbye Channel Changed To {target_channel.name}')
    await message.channel.send(None, embed=embed)
