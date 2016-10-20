async def handdown(cmd, message, args):
    if karaoke:
        if message.author in karaoke_queue:
            karaoke_queue.remove(message.author)
            await cmd.reply('You have been removed from the list!\nWe\'re sorry to see you go, <@' + message.author.id + '>... :cry:')
        else:
            await cmd.reply('I can\'t find you on the list...')
    else:
        await cmd.reply('No karaoke session running')
