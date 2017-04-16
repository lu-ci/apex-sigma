import yaml
import random
import discord
from .mechanics import roll_rarity, make_item_id


async def fish(cmd, message, args):
    with open(cmd.resource('data/fish.yml')) as fish_file:
        fish_data = yaml.safe_load(fish_file)
    rarity = roll_rarity()
    fishie = random.choice(fish_data[rarity])
    fishie.update({'id': make_item_id(message)})
    cmd.db.inv_add(message.author, fishie)
    response = discord.Embed(color=0x1abc9c, title=f'You caught a {fishie["name"]}!')
    await message.channel.send(embed=response)
