async def disconnect(cmd, message, args):
    if cmd.bot.is_voice_connected(message.server):
        voice = cmd.bot.voice_client_in(message.server)
        await voice.disconnect()
    else:
        await cmd.bot.send_message(message.channel, 'I am not connected to any voice channel.')
