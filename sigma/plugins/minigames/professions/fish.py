import random
import discord
import yaml
from config import Currency, Prefix
from .mechanics import roll_rarity, make_item_id
from sigma.core.utils import user_avatar

all_fish = None

visuals = {
    'trash': {
        'icon': '🗑',
        'color': 0x696969
    },
    'common': {
        'icon': '🦐',
        'color': 0xc16a4f
    },
    'uncommon': {
        'icon': '🐟',
        'color': 0x55acee
    },
    'rare': {
        'icon': '🐡',
        'color': 0xd99e82
    },
    'legendary': {
        'icon': '🦑',
        'color': 0xf4abba
    },
    'prime': {
        'icon': '🐠',
        'color': 0xffcc4d
    }
}


async def fish(cmd, message, args):
    global all_fish
    if not all_fish:
        with open(cmd.resource('data/fish.yml')) as fish_file:
            all_fish = yaml.safe_load(fish_file)
    if not cmd.cooldown.on_cooldown(cmd, message):
        cmd.cooldown.set_cooldown(cmd, message, 20)
        kud = cmd.db.get_points(message.author)
        if kud['Current'] >= 20:
            cmd.db.take_points(message.guild, message.author, 20)
            rarity = roll_rarity()
            item = random.choice(all_fish[rarity])
            if 'connector' in item:
                connector = item['connector']
            else:
                if item['name'][0].lower() in ['a', 'e', 'i', 'o', 'u']:
                    connector = 'an'
                else:
                    connector = 'a'
            item_text = f'{connector} {item["name"]}'
            value = item['value']
            if value == 0:
                notify_text = 'You threw it away.\nThis item is **worthless**.'
            else:
                item_id = make_item_id(message)
                item.update({'ItemID': item_id})
                cmd.db.inv_add(message.author, item)
                notify_text = f'This item is valued at **{value} {Currency}**.'
                notify_text += f'\nIt has been added to your inventory.'
                notify_text += f'\nYou can sell it by using the {Prefix}sell command.'
            response = discord.Embed(color=visuals[rarity]['color'])
            response.add_field(name=f'{visuals[rarity]["icon"]} You caught {item_text} of {rarity} quality!',
                               value=notify_text)
            response.set_footer(text=f'You paid 20 {Currency} for the bait.', icon_url=user_avatar(message.author))
        else:
            response = discord.Embed(color=0xDB0000, title=f'You don\'t have enough {Currency}!')
    else:
        timeout = cmd.cooldown.get_cooldown(cmd, message)
        response = discord.Embed(color=0x696969, title=f'🕙 Your new bait will be ready in {timeout} seconds.')
    await message.channel.send(embed=response)
