import discord
from config import permitted_id


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
                    embed = discord.Embed(title=':information_source: Message Recieved', color=0x0099FF)
                    embed.add_field(
                        name=message.author.name + '#' + message.author.discriminator + ' (' + message.author.id + ')',
                        value=message.content)
                    await ev.bot.send_message(user, None, embed=embed)
                    break
