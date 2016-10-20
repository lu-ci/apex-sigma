async def forceunmute(cmd, message, args):
    if checkPermissions(message.author):
        print('Force unmuting')

        await unmutekaraokechannel()
        await cmd.reply("Iterated through channel")
