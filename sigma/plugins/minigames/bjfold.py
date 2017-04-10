import random
import discord
from .black_jack_backend import get_bj, upd_bj, del_bj


async def bjfold(cmd, message, args):
    instance_id = message.guild.id + message.author.id
    instance = get_bj(instance_id)
    if not instance:
        embed = discord.Embed(color=0xDB0000, title='❗ No active blackjack games found for you.')
        await message.channel.send(None, embed=embed)
        return
    deck = instance['Deck']
    p_pts = instance['PlayerScore']
    h_pts = instance['HouseScore']

    if h_pts > p_pts:
        embed = discord.Embed(color=0xDB0000, title='❗ You folded while the dealer was ahead!')
        del_bj(instance['InstanceID'])
        await message.channel.send(None, embed=embed)
        return
    player_drawn = random.choice(deck)
    p_sym, p_suit, p_val = player_drawn
    deck.remove(player_drawn)

    house_drawn = random.choice(deck)
    h_sym, h_suit, h_val = house_drawn
    deck.remove(house_drawn)

    em_p_nam = 'You Drew ' + p_suit + p_sym
    new_p_score = p_pts + p_val
    em_p_val = '```yaml\nYour Score: \n  - ' + str(new_p_score) + '\n```'

    em_h_nam = 'Dealer Drew ' + h_suit + h_sym
    new_h_score = h_pts + h_val
    em_h_val = '```yaml\nHouse Score: \n  - ' + str(new_h_score) + '\n```'

    while new_h_score <= new_p_score:
        bj_data = {
            'InstanceID': instance['InstanceID'],
            'UserID': instance['UserID'],
            'ServerID': instance['ServerID'],
            'Deck': deck,
            'PlayerScore': new_p_score,
            'HouseScore': new_h_score,
            'Bet': instance['Bet'],
            'Ace': False
        }
        instance_data = {instance['InstanceID']: bj_data}
        upd_bj(instance['InstanceID'], instance_data)
        em_h_nam = 'Dealer Drew ' + h_suit + h_sym
        new_h_score += h_val
        em_h_val = '```yaml\nHouse Score: \n  - ' + str(new_h_score) + '\n```'
    if new_h_score > 21:
        prize = (instance['Bet'] // 5) + instance['Bet']
        cmd.db.add_points(message.guild, message.author, prize)
        embed = discord.Embed(color=0x0099FF, title=':gem: The dealer busted out!')
        embed.add_field(name=em_p_nam, value=em_p_val)
        embed.add_field(name=em_h_nam, value=em_h_val)
        embed.set_footer(text='You have been awarded ' + str(prize) + ' points.')
        del_bj(instance['InstanceID'])
        await message.channel.send(None, embed=embed)
    else:
        embed = discord.Embed(color=0xDB0000, title='❗ The dealer overtook you!')
        embed.add_field(name=em_p_nam, value=em_p_val)
        embed.add_field(name=em_h_nam, value=em_h_val)
        del_bj(instance['InstanceID'])
        await message.channel.send(None, embed=embed)
