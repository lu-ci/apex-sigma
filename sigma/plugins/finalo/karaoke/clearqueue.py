async def clearqueue(cmd, message, args):
    if checkPermissions(message.author):
        karaoke_queue.clear()
        await cmd.reply('Karaoke queue cleared')
    else:
        await cmd.reply("Insufficient permissions")
