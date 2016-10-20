async def setchannel(cmd, message, args):
    if checkPermissions(message.author):
        karaoke_channel = message.content[len(pfx) + len('setchannel') + 1:]
        await cmd.reply("Channel set")
