import random
import asyncio


async def choose(cmd, message, args):
    if args:
        choice = random.choice(args)
        out_message = await cmd.bot.send_message(message.channel, 'Uuuuum...')
        await asyncio.sleep(3)
        await cmd.bot.edit_message(out_message, 'I\'ll have to go with **' + choice + '**.')
    else:
        await cmd.bot.send_message(message.channel, cmd.help())
        return
