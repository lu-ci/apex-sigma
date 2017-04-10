import discord


async def sid(cmd, message, args):
    embed = discord.Embed(color=0x0099FF)
    embed.add_field(name='ℹ ' + message.server.name, value='`' + message.server.id + '`')
    await message.channel.send(None, embed=embed)
