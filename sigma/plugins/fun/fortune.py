import discord
import random
import os

fortune_files = []

async def fortune(cmd, message, args):
    if not fortune_files:
        for fortune_file in os.listdir(cmd.resource('fortune')):
            with open(cmd.resource(f'fortune/{fortune_file}')) as forfile:
                text_data = forfile.read()
                fortune_files.append(text_data.split('%'))
    category = random.choice(fortune_files)
    fort = random.choice(category)
    response = discord.Embed(color=0x1ABC9C)
    response.add_field(name='🔮 Fortune', value=f'```\n{fort}\n```')
    await message.channel.send(embed=response)
