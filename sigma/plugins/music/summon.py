from config import Prefix


async def summon(cmd, message, args):
    if not cmd.bot.is_voice_connected(message.server):
        await cmd.bot.join_voice_channel(message.author.voice_channel)
    else:
        await cmd.bot.send_message(message.channel,
                                   'I am already in a voice channel, if you want to move me to yours, use `' + Prefix + 'move`')
