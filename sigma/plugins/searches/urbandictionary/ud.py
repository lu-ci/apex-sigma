import requests
import discord
from config import MashapeKey


async def ud(cmd, message, args):
    ud_input = ' '.join(args)
    url = "https://mashape-community-urban-dictionary.p.mashape.com/define?term=" + ud_input
    headers = {'X-Mashape-Key': MashapeKey, 'Accept': 'text/plain'}
    response = requests.get(url, headers=headers).json()
    result_type = str((response['result_type']))
    if result_type == 'exact':
        definition = str((response['list'][0]['definition']))
        if len(definition) > 750:
            definition = definition[:750] + '...'
        example = str((response['list'][0]['example']))
        embed = discord.Embed(color=0x1abc9c, title='🥃 Urban Dictionary Definition For `' + ud_input + '`')
        embed.add_field(name='Definition', value='```\n' + definition + '\n```')
        embed.add_field(name='Usage Example', value='```\n' + example + '\n```')
        await cmd.bot.send_message(message.channel, None, embed=embed)
