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
    curr_points = cmd.db.get_points(message.server, message.author)
    if curr_points < buyin:
        embed = discord.Embed(color=0xDB0000, title='❗ You don\'t have that many points!')
        await cmd.bot.send_message(message.channel, None, embed=embed)
        return
    cmd.db.take_points(message.server, message.author, buyin)
    instance_id = message.server.id + message.author.id
    bj_instance = get_bj(instance_id)
    if bj_instance:
        embed = discord.Embed(color=0xDB0000, title='❗ A Blackjack Instance For You Already Exists!')
        embed.set_footer(
            text='Use %pfxbjnext to draw the next card, %pfxbjfold to fold the current hand or %pfxbjquit to quit the game.'.replace(
                '%pfx', Prefix))
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
            'ServerID': message.server.id,
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
    await cmd.bot.send_message(message.channel, None, embed=embed)

