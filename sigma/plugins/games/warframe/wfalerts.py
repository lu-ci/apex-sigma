import discord
import aiohttp
from .nodes.alert_functions import parse_alert_data


async def wfalerts(cmd, message, args):
    alert_url = 'https://deathsnacks.com/wf/data/alerts_raw.txt'
    async with aiohttp.ClientSession() as session:
        async with session.get(alert_url) as data:
            alert_data = await data.text()
    alert_list = parse_alert_data(alert_data)
    response = discord.Embed(color=0xFFCC66)
    response.set_author(name='Currently Ongoing Alerts', icon_url='http://i.imgur.com/99ennZD.png')
    for alert in alert_list:
        alert_desc = f'Levels: {alert["levels"]["low"]} - {alert["levels"]["high"]}'
        alert_desc += f'\nLocation: {alert["node"]} ({alert["planet"]})'
        alert_desc += f'\nReward: {alert["rewards"]["credits"]}cr'
        if alert['rewards']['item']:
            alert_desc += f' + {alert["rewards"]["item"]}'
        response.add_field(name=f'Type: {alert["faction"]} {alert["type"]}', value=f'{alert_desc}')
    await message.channel.send(embed=response)
