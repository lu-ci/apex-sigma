import random
import asyncio


async def choose(cmd, message, args):
    if args:
        choice = random.choice(args)
        out_message = await cmd.reply('Uuuuum...')
        await asyncio.sleep(3)
        await cmd.bot.edit_message(out_message, 'I\'ll have to go with **' + choice + '**.')
    else:
        await cmd.reply(cmd.help())
        return
