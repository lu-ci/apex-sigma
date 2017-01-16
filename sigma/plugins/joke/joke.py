import requests
import discord


async def joke(cmd, message, args):
    joke_url = 'http://tambal.azurewebsites.net/joke/random'
    joke_json = requests.get(joke_url).json()
    joke_text = joke_json['joke']
    embed = discord.Embed(color=0x1abc9c)
    embed.add_field(name='😆 Have A Random Joke', value='\n```' + joke_text + '\n```')
    await cmd.bot.send_message(message.channel, None, embed=embed)
