import asyncio
from cleverbot import Cleverbot

cb = Cleverbot()

async def cleverbot(ev, message, args):
    mention = '<@' + ev.bot.user.id + '>'
    mention_alt = '<@!' + ev.bot.user.id + '>'
    author_id = message.author.id
    if message.content.startswith(mention) or message.content.startswith(mention_alt):
        await ev.typing()

        try:
            cb_input = message.content[len(mention) + 1:]
            response = cb.ask(cb_input)
            await asyncio.sleep(len(response) * 0.0145)
            await ev.reply('<@' + message.author.id + '> ' + response)
        except:
            msg = 'Sorry <@{:s}>, my brain isn\'t working at the moment give me some time to catch my breath...'
            await ev.reply(msg.format(author_id))
