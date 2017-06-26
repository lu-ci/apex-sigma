import json
import random
import discord


async def dadjoke(cmd, message, args):
    with open(cmd.resource('dadjokes.json'), 'r', encoding='utf-8') as dadjokes_file:
        jokes = dadjokes_file.read()
        jokes = json.loads(jokes)
        joke_list = jokes['JOKES']
        end_joke_choice = random.choice(joke_list)
        end_joke = end_joke_choice['setup']
        punchline = end_joke_choice['punchline']
        embed = discord.Embed(color=0x1abc9c)
        embed.add_field(name='😖 Have An Awful Dad Joke', value=f'```yaml\n\"{end_joke}... {punchline}\"\n```')
        await message.channel.send(None, embed=embed)
