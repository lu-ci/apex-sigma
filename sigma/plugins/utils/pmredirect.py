from config import permitted_id

from sigma.core.formatting import codeblock


async def pmredirect(ev, message, args):
    cid = ev.bot.user.id
    author = message.author

    if not message.server:
        if author.id == cid or author.id in permitted_id:
            return
        else:
            ev.log.info('User {:s} [{:s}] sent a private message.'.format(author.name, author.id))

            # very expensive operation
            for user in ev.bot.get_all_members():
                if user.id == permitted_id[0]:
                    private_msg_to_owner = await ev.bot.start_private_message(user=user)
                    msg = '**{:s}** (ID: {:s}):\n{:s}\n'
                    await ev.bot.send_message(private_msg_to_owner, msg.format(
                        author.name, author.id, codeblock(message.content)))
                    break
