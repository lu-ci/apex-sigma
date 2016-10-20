async def takemic(cmd, message, args):
    if not karaoke_deban[0]:  # if its not someone's else turn
        if message.author in karaoke_queue:  # if user is in the queue
            if message.author == karaoke_queue[0]:  # if its his/her turn
                he_is = await isuserinvoicechannel(karaoke_channel, karaoke_queue[0])
                if he_is:
                    karaoke_deban = [True, karaoke_queue.popleft()]

                    await lookforstrayspotlight(message.server)
                    await assignspotlight(karaoke_deban[1])
                    await cmd.reply(
                                                   '<@' + karaoke_deban[
                                                       1].id + '> is morally ready, enforcing strict mode')
                    await enforcestrictmode()
                    await cmd.bot.server_voice_state(karaoke_deban[1], mute=False)
                    return
                else:
                    cmd.reply('<@' + karaoke_queue[0].id + "> you're not in karaoke channel")
            else:
                await cmd.reply("<@" + message.author.id + "> it's not your turn yet")
        else:
            await cmd.reply("<@" + message.author.id + "> you're not in the queue")
    else:
        cmd.reply("Shh, it's <@" + karaoke_deban[1].id + "> singing time")
