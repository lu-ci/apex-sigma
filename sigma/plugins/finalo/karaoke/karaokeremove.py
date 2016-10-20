async def karaokeremove(cmd, message, args):
    if checkPermissions(message.author):
        target = ' '.join(args)

        if (len(target)) == 0:
            await cmd.reply("No user specified, aborting")
            return
        if message.mentions[0] in karaoke_queue:
            karaoke_queue.remove(message.mentions[0])
            await cmd.reply('User removed from the queue')
        else:
            await cmd.reply('User not found in the queue')
    else:
        await cmd.reply("Insufficient permissions")
