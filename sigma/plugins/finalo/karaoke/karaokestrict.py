async def karaokestrict(cmd, message, args):
    if checkPermissions(message.author):
        if karaoke_strict:
            karaoke_strict = False
            await unmutekaraokechannel()
            await cmd.reply("Strict mode disabled")
        else:
            await enforcestrictmode()
            await cmd.reply("Strict mode enabled")
    else:
        await cmd.reply("Insufficient permissions")
