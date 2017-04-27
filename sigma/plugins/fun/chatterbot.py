import discord
from sigma.core.permission import check_admin


async def chatterbot(cmd, message, args):
    if not check_admin(message.author, message.channel):
        embed = discord.Embed(title='⛔ Unpermitted. Server Admin Only.', color=0xDB0000)
    else:
        active = cmd.db.get_settings(message.guild.id, 'CleverBot')
        if active:
            cmd.db.set_settings(message.guild.id, 'CleverBot', False)
            state = '**Disabled**.'
        else:
            cmd.db.set_settings(message.guild.id, 'CleverBot', True)
            state = '**Enabled**.'
        embed = discord.Embed(title='✅ CleverBot Feature Has Been ' + state + '.', color=0x66CC66)
    await message.channel.send(None, embed=embed)
