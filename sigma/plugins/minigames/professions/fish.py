import discord
from config import Currency
from .mechanics import roll_rarity

values = {
    'trash': 0,
    'common': 30,
    'uncommon': 50,
    'rare': 80,
    'legendary': 100
}

async def fish(cmd, message, args):
    if not cmd.cooldown.on_cooldown(cmd, message):
        cmd.cooldown.set_cooldown(cmd, message, 60)
        kud = cmd.db.get_points(message.author)
        if kud['Current'] >= 20:
            cmd.db.take_points(message.guild, message.author, 20)
            rarity = roll_rarity()
            if rarity == 'trash':
                icon = '👢'
                text = 'You reeled in some trash'
            else:
                icon = '🐟'
                text = f'You caught a {rarity} fish'
            cmd.db.add_points(message.guild, message.author, values[rarity])
            response = discord.Embed(color=0x1ABC9C, title=f'{icon} {text} earning you `{values[rarity]} {Currency}`!')
        else:
            response = discord.Embed(color=0xDB0000, title=f'You don\'t have enough {Currency}!')
    else:
        timeout = cmd.cooldown.get_cooldown(cmd, message)
        response = discord.Embed(color=0x696969, title=f'🕙 Your new bait will be ready in {timeout} seconds.')
    await message.channel.send(embed=response)
