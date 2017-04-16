import discord
from config import Currency
from .mechanics import roll_rarity

values = {
    'trash': 0,
    'common': 30,
    'uncommon': 50,
    'rare': 100,
    'legendary': 200
}

async def fish(cmd, message, args):
    kud = cmd.db.get_points(message.author)
    if kud['Current'] >= 20:
        rarity = roll_rarity()
        if rarity == 'trash':
            icon = '👢'
            text = 'You reeled in some trash.'
        else:
            icon = '🐟'
            text = f'You caught a {rarity} fish!'
        cmd.db.add_points(message.guild, message.author, values[rarity])
        response = discord.Embed(color=0x1ABC9C, title=f'{icon} {text} which earned you {values[rarity]} {Currency}!')
    else:
        response = discord.Embed(color=0xDB0000, title=f'You don\'t have enough {Currency}!')
    await message.channel.send(embed=response)
