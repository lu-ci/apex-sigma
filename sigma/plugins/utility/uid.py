import discord


async def uid(cmd, message, args):
    if message.mentions:
        user_q = message.mentions[0]
    else:
        user_q = message.author
    embed = discord.Embed(color=0x0099FF)
    embed.add_field(name='ℹ ' + user_q.name, value='`' + user_q.id + '`')
    await cmd.bot.send_message(message.channel, None, embed=embed)
