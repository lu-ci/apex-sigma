import discord
import aiohttp
import json


async def analyze(cmd, message, args):
    if args:
        text = ' '.join(args)
        url = 'http://text-processing.com/api/sentiment/'
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data={'text': text}) as data:
                data = await data.read()
                data = json.loads(data)
                prob = data['probability']
        response = discord.Embed(color=0x1ABC9C)
        response.add_field(name='Given Text', value=f'```\n{text}\n```', inline=False)
        response.add_field(name='Positive', value=f'```py\n{str(prob["pos"])[:4]}\n```', inline=True)
        response.add_field(name='Neutral', value=f'```py\n{str(prob["neutral"])[:4]}\n```', inline=True)
        response.add_field(name='Negative', value=f'```py\n{str(prob["neg"])[:4]}\n```', inline=True)
        response.add_field(name='Verdict', value=f'```\n{data["label"].title()}\n```', inline=False)
        await message.channel.send(embed=response)
