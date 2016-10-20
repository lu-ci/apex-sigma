import json
import asyncio
import random


async def dadjoke(cmd, message, args):
    with open('storage/dadjokes.json', 'r', encoding='utf-8') as dadjokes_file:
        jokes = dadjokes_file.read()
        jokes = json.loads(jokes)
        joke_list = jokes['JOKES']
        end_joke_choice = random.choice(joke_list)
        end_joke = (end_joke_choice['setup'])
        punchline = ('\n\n' + end_joke_choice['punchline'])
        joke_msg = await cmd.reply('I can\'t believe I\'m doing this...\n```' + end_joke + '```')
        await asyncio.sleep(3)
        await cmd.bot.edit_message(joke_msg, 'I can\'t believe I\'m doing this...\n```' + end_joke + punchline + '```')
