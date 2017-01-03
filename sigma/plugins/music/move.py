from config import Prefix


async def move(cmd, message, args):
    if not cmd.bot.is_voice_connected(message.server):
        await cmd.bot.send_message(message.channel, 'I am not in a voice channel, you need to `' + Prefix + 'summon` me first.')
    else:
        voice = cmd.bot.voice_client_in(message.server)
        await voice.move_to(message.author.voice_channel)
