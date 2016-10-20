async def handup(cmd, message, args):
    if karaoke:
        if message.author.id not in karaoke_queue:
            karaoke_queue.append(message.author)
            await cmd.reply('<@' + message.author.id + '> has joined the singers list!\nA round of applause please! :musical_note: :clap:')
        else:
            await cmd.reply('I\'m sorry <@' + message.author.id + '>, but you\'re already on the list...')
    else:
        await cmd.reply('No karaoke session running')
