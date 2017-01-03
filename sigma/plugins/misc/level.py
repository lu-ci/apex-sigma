import discord


async def level(cmd, message, args):
    if message.mentions:
        target = message.mentions[0]
    else:
        target = message.author
    user_id = target.id
    query = {
        'UserID': user_id,
        'ServerID': message.server.id
    }
    number_grabber = cmd.db.find('PointSystem', query)
    points = 0
    for result in number_grabber:
        try:
            points = result['Points']
        except:
            pass
    level_num = points / 1690
    points = str(points)
    level_num = str(level_num).split('.')[0]
    embed = discord.Embed(title=':gem: Sigma Ranking For ' + target.name, color=0x0099FF)
    embed.add_field(name='Level', value=str(level_num))
    embed.add_field(name='Points', value=str(points))
    await cmd.bot.send_message(message.channel, None, embed=embed)
