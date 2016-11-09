import wolframalpha
from config import WolframAlphaAppID

async def wa(cmd, message, args):
    if not args:
        await cmd.bot.send_message(message.channel, cmd.help())
        return
    else:
        wa_q = ' '.join(args)
        wac = wolframalpha.Client(WolframAlphaAppID)
        results = wac.query(wa_q)
        try:
            result = (next(results.results).text)
        except StopIteration:
            await cmd.bot.send_message(message.channel, 'Error, not a mathematical problem.')
            return
        await cmd.bot.send_message(message.channel, 'Results:\n```' + result + '\n```')
