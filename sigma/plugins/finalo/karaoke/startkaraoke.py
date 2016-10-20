async def startkaraoke(cmd, message, args):
    if checkPermissions(message.author):
        if karaoke_mod:
            karaoke_mod = False
            await self.client.send_message(message.channel, "Karaoke mode is set to false, not muting users")
        else:
            karaoke_mod = True
            await cmd.reply("Karaoke mode is set to true, muting users")
    else:
        await cmd.reply("Insufficient permissions")

    if checkPermissions(message.author):
        target = ' '.join(args)

        if (len(target)) == 0:
            await cmd.reply("No channel specified, aborting")
            return

        global karaoke, karaoke_channel, karaoke_strict
        try:
            karaoke = True
            karaoke_channel = target
            # karaoke_strict = True
            # try:
            await lookforstrayspotlight(message.server)
            await enforcestrictmode()
            await cmd.reply("Karaoke started in strict mode on channel " + karaoke_channel)

        except SyntaxError:
            await cmd.reply("Error while starting karaoke session")
    else:
        await cmd.reply("Insufficient permissions")
