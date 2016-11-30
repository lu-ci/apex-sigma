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
            await cmd.bot.send_message(message.channel, 'We ran into an error, we were unable to process that.')
            return
        await cmd.bot.send_message(message.channel, 'Results:\n```' + result + '\n```')
