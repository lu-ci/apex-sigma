import cleverbot

sigma = cleverbot.Cleverbot()


async def cleverbot_control(ev, message, args):
    active = ev.db.get_settings(message.server.id, 'CleverBot')
    if active:
        ev.db.add_stats('CBCount')
        mention = '<@' + ev.bot.user.id + '>'
        mention_alt = '<@!' + ev.bot.user.id + '>'
        if message.content.startswith(mention) or message.content.startswith(mention_alt):
            response = sigma.ask(' '.join(args[1:]))
            await ev.bot.send_message(message.channel, message.author.mention + ' ' + response)
