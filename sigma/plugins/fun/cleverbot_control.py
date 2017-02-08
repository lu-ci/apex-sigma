from cleverbot import Cleverbot

cb = Cleverbot('Apex-Sigma')


async def cleverbot_control(ev, message, args):
    active = ev.db.get_settings(message.server.id, 'CleverBot')
    if active:
        ev.db.add_stats('CBCount')
        mention = '<@' + ev.bot.user.id + '>'
        mention_alt = '<@!' + ev.bot.user.id + '>'
        if message.content.startswith(mention) or message.content.startswith(mention_alt):
            await ev.bot.send_typing(message.channel)

            if message.content.startswith(mention):
                cb_input = message.content[len(mention) + 1:]
            elif message.content.startswith(mention_alt):
                cb_input = message.content[len(mention_alt) + 1:]
            else:
                return
            response = cb.ask(cb_input)
            await ev.bot.send_message(message.channel, '<@' + message.author.id + '> ' + response)
