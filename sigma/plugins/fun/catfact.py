import aiohttp
import discord


async def catfact(cmd, message, args):
        resource = 'http://catfacts-api.appspot.com/api/facts'
        async with aiohttp.ClientSession() as session:
            async with session.get(resource) as data:
                data = await data.json()
        fact = data['facts'][0]
        embed = discord.Embed(color=0x1abc9c)
        embed.add_field(name=':cat: Did you know...', value='```\n' + fact + '\n```')
        await cmd.bot.send_message(message.channel, None, embed=embed)
