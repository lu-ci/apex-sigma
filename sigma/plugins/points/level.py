import discord
from sigma.core.utils import user_avatar


async def level(cmd, message, args):
    if message.mentions:
        target = message.mentions[0]
    else:
        target = message.author
    point_data = cmd.db.get_points(target)
    if point_data:
        total_pts = point_data['Total']
        current_pts = point_data['Current']
        servers = point_data['Servers']
        curr_srv = 0
        if message.server.id in servers:
            curr_srv = servers[message.server.id]
        response = discord.Embed(color=0x1ABC9C)
        response.set_author(name=f'{target.name}\'s Currency Data', icon_url=user_avatar(target))
        response.add_field(name='Currently', value=f'```\n{current_pts}\n```')
        response.add_field(name='Total', value=f'```\n{total_pts}\n```')
        response.add_field(name='This Server', value=f'```\n{curr_srv}\n```')
    else:
        response = discord.Embed(color=0x696969, title=f'🔍 I couldn\'t find {target.name} in my point database.')
    await cmd.bot.send_message(message.channel, None, embed=response)
