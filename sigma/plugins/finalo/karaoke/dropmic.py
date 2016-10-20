async def dropmic(cmd, message, args):
    if karaoke_deban[0]:
        if message.author == karaoke_deban[1]:
            karaoke_strict = False
            await unmutekaraokechannel()
            await cmd.reply('It seems <@' + karaoke_deban[ 1].id +
                            '> is done, unfortunatelly at the cost of a broken microphone!\nWe broudght spares, yay~! Whenever the next singer is ready, type ' + bold(
                            pfx) + bold('takemic') + '!')
            karaoke_deban = [False, 0]
            return
        else:
            print('1')
            await cmd.reply("What do you think you're dropping <@" + message.author.id + "> ?")
    else:
        print('2')
        await cmd.reply("What do you think you're dropping <@" + message.author.id + "> ?")
