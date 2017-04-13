import discord
from sigma.core.utils import user_avatar
from config import Currency


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
        if str(message.guild.id) in servers:
            curr_srv = servers[str(message.guild.id)]
        response = discord.Embed(color=0x1ABC9C)
        response.set_author(name=f'{target.name}\'s Currency Data', icon_url=user_avatar(target))
        response.add_field(name='Current Wallet', value=f'```py\n{current_pts} {Currency}\n```')
        response.add_field(name='This Server', value=f'```py\n{curr_srv} {Currency}\n```')
        response.add_field(name='Total Gained', value=f'```py\n{total_pts} {Currency}\n```')
    else:
        response = discord.Embed(color=0x696969, title=f'🔍 I couldn\'t find {target.name} in my point database.')
    response.set_footer(text=f'{Currency} can be earned by being an active member of the server.')
    await message.channel.send(None, embed=response)
