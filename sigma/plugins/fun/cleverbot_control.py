import cleverwrap
from config import CleverBotAPIKey

sigma = cleverwrap.CleverWrap(CleverBotAPIKey)


async def cleverbot_control(ev, message, args):
    active = ev.db.get_settings(message.server.id, 'CleverBot')
    if active:
        ev.db.add_stats('CBCount')
        mention = '<@' + ev.bot.user.id + '>'
        mention_alt = '<@!' + ev.bot.user.id + '>'
        if message.content.startswith(mention) or message.content.startswith(mention_alt):
            interaction = ' '.join(args[1:])
            try:
                response = sigma.say(interaction)
            except:
                try:
                    sigma.reset()
                    response = sigma.say(interaction)
                except:
                    response = ' I\'m sorry I seem to be unable to think straight at the moment...'
            await ev.bot.send_message(message.channel, message.author.mention + ' ' + response)
