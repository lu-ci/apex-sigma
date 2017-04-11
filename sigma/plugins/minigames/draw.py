import random
import discord


async def draw(cmd, message, args):
    embed = discord.Embed(color=0x1ABC9C)
    if not args:
        amount = 2
    else:
        try:
            amount = int(args[0])
        except:
            embed.set_footer(text='Not a number, defaulted to 2.')
            amount = 2
    if amount > 10:
        amount = 2
        embed.set_footer(text='Number exceeded the limit of 10, defaulted to 2.')
    sign_list = [':spades:', ':hearts:', ':clubs:', ':diamonds:']
    n = 0
    while n < amount:
        n += 1
        card_number = random.randint(1, 14)
        if card_number == 11 or card_number == 1:
            card_number = 'Ace'
        elif card_number == 12:
            card_number = 'Jack'
        elif card_number == 13:
            card_number = 'Queen'
        elif card_number == 14:
            card_number = 'King'
        else:
            card_number = str(card_number)
        card_sign = random.choice(sign_list)
        combination = '**' + card_number + '** - ' + card_sign
        embed.add_field(name= 'Card #' + str(n), value=combination)
    await message.channel.send(None, embed=embed)
