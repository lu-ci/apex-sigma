import wikipedia

from sigma.core.formatting import code, codeblock


async def wiki(cmd, message, args):
    q = ' '.join(args).lower()

    result = wikipedia.summary(q)

    if result is not None:
        if len(result) >= 650:
            result = result[:650] + ' ...'

        out_text = 'Your search results for {:s}:\n{:s}'.format(
                code(q), codeblock(result))
    else:
        out_text = 'Nothing could be found...'

    await cmd.bot.send_message(message.channel, out_text)
