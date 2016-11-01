import random

async def rps(cmd, message, args):
    if not args:
        await cmd.reply(cmd.help())
        return
    else:
        sign_list = ['rock', 'paper', 'scissors']
        my_choice = random.choice(sign_list)
        out_text = 'I choose **' + my_choice + '**!'
        if args[0].lower().startswith('r'):
            their_choice = 'rock'
            counter = 'paper'
        elif args[0].lower().startswith('p'):
            their_choice = 'paper'
            counter = 'scissors'
        elif args[0].lower().startswith('s'):
            their_choice = 'scissors'
            counter = 'rock'
        else:
            await cmd.reply('Unrecognized sign choice.')
            return
        if my_choice == their_choice:
            out_text += '\nIt\'s a **Draw**!'
        elif my_choice == counter:
            out_text += '\n**I win**! So sorry~ :second_place:'
        else:
            out_text += '\nCongrats! **You won**! :first_place:'
        await cmd.reply(out_text)
