import datetime
import discord
import aiohttp
import arrow
import json

tier_names = {
    'VoidT1': 'Lith',
    'VoidT2': 'Meso',
    'VoidT3': 'Neo',
    'VoidT4': 'Axi'
}

async def wffissures(cmd, message, args):
    fissure_url = 'https://deathsnacks.com/wf/data/activemissions.json'
    async with aiohttp.ClientSession() as session:
        async with session.get(fissure_url) as data:
            fissure_data = await data.read()
            fissure_list = json.loads(fissure_data)
    response = discord.Embed(color=0x66ccff)
    response.set_author(name='Current Ongoing Fissures', icon_url='https://i.imgur.com/vANGxqe.png')
    for fis in fissure_list:
        relic_tier = tier_names[fis['Modifier']]
        fis_desc = f'Location: {fis["Node"]}'
        time_left = fis['Expiry']['sec'] - arrow.utcnow().timestamp
        death_time = str(datetime.timedelta(seconds=time_left))
        fis_desc += f'\nDisappears In: {death_time}'
        response.add_field(name=f'{relic_tier} Void Fissure', value=fis_desc)
    response.set_footer(text='Timers are not updated live.')
    await message.channel.send(embed=response)
