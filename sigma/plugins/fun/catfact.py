import aiohttp
import discord
import secrets
import json


async def catfact(cmd, message, args):
        resource = 'http://www.catfact.info/api/v1/facts.json?page=0&per_page=700'
        async with aiohttp.ClientSession() as session:
            async with session.get(resource) as data:
                data = await data.read()
                data = json.loads(data)
        fact = secrets.choice(data['facts'])
        embed = discord.Embed(color=0x1abc9c)
        embed.add_field(name=':cat: Did you know...', value='```\n' + fact['details'] + '\n```')
        await message.channel.send(None, embed=embed)
