import requests
import discord


async def catfact(cmd, message, args):
        resource = 'http://catfacts-api.appspot.com/api/facts'
        data = requests.get(resource).json()
        fact = data['facts'][0]
        embed = discord.Embed(color=0x1abc9c)
        embed.add_field(name=':cat: Did you know...', value='```\n' + fact + '\n```')
        await cmd.bot.send_message(message.channel, None, embed=embed)
