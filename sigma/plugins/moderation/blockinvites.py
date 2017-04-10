import discord
from sigma.core.permission import check_admin


async def blockinvites(cmd, message, args):
    if not check_admin(message.author, message.channel):
        embed = discord.Embed(title='⛔ Unpermitted. Server Admin Only.', color=0xDB0000)
    else:
        active = cmd.db.get_settings(message.guild.id, 'BlockInvites')
        if active:
            cmd.db.set_settings(message.guild.id, 'BlockInvites', False)
            embed = discord.Embed(color=0x66CC66, title='✅ Invite Blocking Has Been Disabled')
        else:
            cmd.db.set_settings(message.guild.id, 'BlockInvites', True)
            embed = discord.Embed(color=0x66CC66, title='✅ Invite Blocking Has Been Enabled')
    await message.channel.send(None, embed=embed)


