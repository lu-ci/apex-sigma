import cleverwrap
from config import CleverBotAPIKey

cw = cleverwrap.CleverWrap(CleverBotAPIKey)


async def chatterbot_control(ev, message, args):
    active = ev.db.get_settings(message.guild.id, 'CleverBot')
    if active:
        mention = f'<@{ev.bot.user.id}>'
        mention_alt = f'<@!{ev.bot.user.id}>'
        if message.content.startswith(mention) or message.content.startswith(mention_alt):
            interaction = ' '.join(args[1:])
            if message.mentions:
                for mnt in message.mentions:
                    interaction = interaction.replace(mnt.mention, mnt.name)
            try:
                response = str(cw.say(interaction))
            except:
                cw.reset()
                response = str(cw.say(interaction))
            await message.channel.send(message.author.mention + ' ' + response)
