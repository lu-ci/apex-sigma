import yaml
import random
import discord
from .mechanics import roll_rarity, make_item_id

fish_data = None

async def fish(cmd, message, args):
    global fish_data
    if not fish_data:
        with open(cmd.resource('data/fish.yml')) as fish_file:
            fish_data = yaml.safe_load(fish_file)
    inv = cmd.db.get_inv(message.author)
    if len(inv) < 25:
        rarity = roll_rarity()
        fishie = random.choice(fish_data[rarity])
        fishie.update({'id': make_item_id(message)})
        cmd.db.inv_add(message.author, fishie)
        connector = 'a'
        for letter in ['a', 'e', 'i', 'o', 'u']:
            if fishie.name.startswith(letter):
                connector = 'an'
                break
        if fishie['name'].startswith()
        response = discord.Embed(color=0x1ABC9C, title=f'You caught {connector} {fishie["name"]}!')
    else:
        response = discord.Embed(color=0xDB0000)
    await message.channel.send(embed=response)

