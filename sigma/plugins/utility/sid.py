import discord


async def sid(cmd, message, args):
    embed = discord.Embed(color=0x0099FF)
    embed.add_field(name=':information_source: ' + message.server.name, value='`' + message.server.id + '`')
    await cmd.bot.send_message(message.channel, None, embed=embed)
