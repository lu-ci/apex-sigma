import random
import discord
from config import Currency, permitted_id
from .mechanics import roll_rarity, make_item_id, get_all_items, get_items_in_rarity
from sigma.core.utils import user_avatar

all_fish = None


async def fish(cmd, message, args):
    global all_fish
    if not all_fish:
        all_fish = get_all_items('fish', cmd.resource('data'))
    if not cmd.cooldown.on_cooldown(cmd, message):
        cmd.cooldown.set_cooldown(cmd, message, 60)
        kud = cmd.db.get_points(message.author)
        if kud['Current'] >= 20:
            cmd.db.take_points(message.guild, message.author, 20)
            rarity = roll_rarity()
            if args:
                if message.author.id in permitted_id:
                    try:
                        rarity = int(args[0])
                    except TypeError:
                        pass
            all_items_in_rarity = get_items_in_rarity(all_fish, rarity)
            item = random.choice(all_items_in_rarity)
            value = item.value
            connector = 'a'
            if item.rarity_name[0].lower() in ['a', 'e', 'i', 'o', 'u']:
                connector = 'an'
            if value == 0:
                response_title = f'{item.icon} You caught {connector} {item.name} and threw it away!'
            else:
                response_title = f'{item.icon} You caught {connector} {item.rarity_name} {item.name}!'
                item_id = make_item_id(message)
                data_for_inv = {
                    'name': item.name,
                    'value': item.value,
                    'description': item.description,
                    'rarity': item.rarity,
                    'rarity_name': item.rarity_name,
                    'item_id': item_id,
                    'item_file_id': item.item_file_id,
                    'item_type': item.item_type,
                    'color': item.color,
                    'icon': item.icon
                }
                cmd.db.inv_add(message.author, data_for_inv)
            response = discord.Embed(color=item.color, title=response_title)
            response.set_author(name=message.author.display_name, icon_url=user_avatar(message.author))
        else:
            response = discord.Embed(color=0xDB0000, title=f'❗ You don\'t have enough {Currency}!')
    else:
        timeout = cmd.cooldown.get_cooldown(cmd, message)
        response = discord.Embed(color=0x696969, title=f'🕙 Your new bait will be ready in {timeout} seconds.')
    await message.channel.send(embed=response)
