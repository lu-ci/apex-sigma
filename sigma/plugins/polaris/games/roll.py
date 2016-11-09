import random


async def roll(cmd, message, args):
    if args:
        try:
            number = random.randint(0, int(args[0].replace('-', '')))
        except Exception as e:
            cmd.log.error(e)
            await cmd.bot.send_message(message.channel, 'Only numbers are accepted for the end range.')
            return
    else:
        number = random.randint(0, 100)
    num = str(number)
    if len(num) > 1950:
        num = num[:1950] + '...'
    out_text = 'That\'s a lovely `' + num + '` you\'ve rolled there!'
    await cmd.bot.send_message(message.channel, out_text)
