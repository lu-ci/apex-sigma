async def stopkaraoke(cmd, message, args):
    if checkPermissions(message.author):
        if karaoke:
            karaoke = False
            temp = []

            for channel in message.server.channels:  # iterate through server channels
                if channel.name == karaoke_channel:  # find the karaoke channel
                    for user in channel.voice_members:  # iterate through users in the channel
                        temp.append(user)

                    break

            for user in temp:
                await cmd.bot.server_voice_state(user, mute=False)  # unmute them

            await cmd.reply("Karaoke stopped")
        else:
            await cmd.reply("No ongoing karaoke found")
    else:
        await cmd.reply("Insufficient permissions")
