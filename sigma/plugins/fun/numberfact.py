import random
import aiohttp
import discord

async def numberfact(cmd, message, args):
    types = ['trivia', 'date', 'math', 'year']
    ran_type = random.choice(types)
    embed = discord.Embed(color=0x1abc9c)
    if not args:
        url = 'http://numbersapi.com/random/' + ran_type + '?json'
    else:
        number = args[0]
        if len(args) > 1:
            fact_type = args[1]
            fact_type = fact_type.lower()
            if fact_type not in types:
                fact_type = ran_type
                embed.set_footer(text='Invalid fact type, defaulted to random.')
        else:
            fact_type = ran_type
        url = 'http://numbersapi.com/' + number + '/' + fact_type + '?json'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as data:
            data = await data.json()
    fact = data['text']
    embed.add_field(name=':four: Number Fact', value='```\n' + fact + '\n```')
    await message.channel.send(None, embed=embed)
