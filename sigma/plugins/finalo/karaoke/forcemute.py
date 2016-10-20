async def forcemute(cmd, message, args):
    if checkPermissions(message.author):
        print('Force muting')
        await mutekaraokechannel()
        await cmd.reply("Iterated through channel")
