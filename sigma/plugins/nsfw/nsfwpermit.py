import discord
from sigma.core.permission import check_admin, set_channel_nsfw


async def nsfwpermit(cmd, message, args):
    channel = message.channel

    if check_admin(message.author, channel):
        if set_channel_nsfw(cmd.db, channel.id):
            embed = discord.Embed(color=0x9933FF,
                                  title=':eggplant: The NSFW Module has been Enabled for ' + channel.name)
        else:
            embed = discord.Embed(color=0xFF9900, title=':fire: The NSFW Module has been Disabled for ' + channel.name)
    else:
        embed = discord.Embed(type='rich', color=0xDB0000, title='⛔ Insufficient Permissions. Server Admin Only.')
    await message.channel.send(None, embed=embed)
