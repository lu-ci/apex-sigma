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
        result = ''
        try:
            for res in results.results:
                if int(res['@numsubpods']) == 1:
                    result += '\n' + res['@title'] + ': ' + res['subpod']['plaintext']
                else:
                    result += '\n' + res['@title'] + ': ' + res['subpod'][0]['img']['@title']
        except Exception as e:
            cmd.log.error(e)
            await cmd.bot.send_message(message.channel, 'We ran into an error, we were unable to process that.\n' + str(e))
            return
        if len(result) > 1950:
            result = result[:1950]
        await cmd.bot.send_message(message.channel, 'Results:\n```' + result + '\n```')
