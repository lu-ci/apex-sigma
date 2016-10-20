async def listchannelmembers(cmd, message, args):
    if checkPermissions(message.author):
        for channel in message.server.channels:  # iterate through server channels
            if channel.name == karaoke_channel:  # find the karaoke channel
                for user in channel.voice_members:  # iterate through users in the channel
                    print(user.name)
