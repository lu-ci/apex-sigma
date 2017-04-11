import discord

async def userinfo(cmd, message, args):
    out_list = []
    if args:
        user_q = message.mentions[0]
    else:
        user_q = message.author

    out_list.append(['Username', user_q.name + '#' + user_q.discriminator])
    out_list.append(['User ID', user_q.id])
    if user_q.nick:
        out_list.append(['Nickname', user_q.nick])
    out_list.append(['Joined', str(user_q.created_at)])
    out_list.append(['Status', str(user_q.status).replace('dnd', 'do not disturb').title()])
    if user_q.game:
        out_list.append(['Playing', str(user_q.game).title()])
    if user_q.roles is not None:
        out_list.append(['Top Role', str(user_q.top_role)])
    out_list.append(['Color', str(user_q.color).upper()])
    out_list.append(['Is Bot', user_q.bot])

    embed = discord.Embed(title=user_q.name + ' Information', color=user_q.color)
    for item in out_list:
        embed.add_field(name=str(item[0]), value='```python\n' + str(item[1]) + '\n```')

    await message.channel.send(None, embed=embed)
