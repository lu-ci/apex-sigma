import discord
from sigma.core.permission import check_kick


async def unwarn(cmd, message, args):
    if not check_kick(message.author, message.channel):
        out_content = discord.Embed(color=0xDB0000,
                                    title='⛔ Users With Kick Permissions Only.')
        await message.channel.send(None, embed=out_content)
        return
    if not args or not message.mentions:
        return
    target = message.mentions[0]
    try:
        warned_users = cmd.db.get_settings(message.guild.id, 'WarnedUsers')
    except KeyError:
        cmd.db.set_settings(message.guild.id, 'WarnedUsers', {})
        warned_users = {}
    if target.id in warned_users:
        del warned_users[target.id]
        cmd.db.set_settings(message.guild.id, 'WarnedUsers', warned_users)
        response = discord.Embed(color=0x66CC66, title=f'✅ {target.name} has been removed from the warning list.')
    else:
        response = discord.Embed(color=0x0099FF, title=f'ℹ {target.name} is not in the list of warned users.')
    await message.channel.send(None, embed=response)
