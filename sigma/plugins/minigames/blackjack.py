import discord
import random
from config import Prefix
from .black_jack_backend import get_bj, add_bj, symbols, suits


async def blackjack(cmd, message, args):
    try:
        buyin = abs(int(args[0]))
        if buyin < 5:
            buyin = 5
    except:
        buyin = 20
    curr_points = cmd.db.get_points(message.author)['Current']
    if curr_points < buyin:
        embed = discord.Embed(color=0xDB0000, title='❗ You don\'t have that many points!')
        await message.channel.send(None, embed=embed)
        return
    cmd.db.take_points(message.guild, message.author, buyin)
    instance_id = message.guild.id + message.author.id
    bj_instance = get_bj(instance_id)
    if bj_instance:
        embed = discord.Embed(color=0xDB0000, title='❗ A Blackjack Instance For You Already Exists!')
        embed.set_footer(
            text=f'Use {Prefix}bjnext to draw the next card, {Prefix}bjfold to fold the current hand or {Prefix}bjquit to quit the game.')
    else:
        deck = []
        for symbol in symbols:
            for suit in suits:
                try:
                    value = int(suit)
                except:
                    value = 10
                deck.append([symbol, suit, value])
        bj_data = {
            'InstanceID': instance_id,
            'UserID': message.author.id,
            'ServerID': message.guild.id,
            'Deck': deck,
            'PlayerScore': 0,
            'HouseScore': 0,
            'Bet': buyin,
            'Ace': False
        }
        instance_data = {instance_id: bj_data}
        add_bj(instance_id, instance_data)
        embed = discord.Embed(color=0x1abc9c,
                              title=random.choice(symbols) + ' A BlackJack Instance Has Been Created For You.')
        embed.set_footer(text='The set buyin amount is ' + str(buyin))
    await message.channel.send(None, embed=embed)
