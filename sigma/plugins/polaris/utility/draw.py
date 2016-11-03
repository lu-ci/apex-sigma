import random


async def draw(cmd, message, args):
    if not args:
        amount = 2
    else:
        try:
            amount = int(args[0])
        except:
            await cmd.reply('Not a number, defaulting to 2...')
            amount = 2
    if amount > 10:
        amount = 2
        await cmd.reply('Number exceeds the limit of 10, defaulting to 2...')
    sign_list = [':spades:', ':hearts:', ':clubs:', ':diamonds:']
    n = 0
    out_text = 'Your cards are:'
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
        out_text += '\n' + combination
    await cmd.reply(out_text)
