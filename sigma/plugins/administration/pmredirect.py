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
            embed = discord.Embed(color=0x0099FF)
            embed.add_field(name='{:s} Sent a Message'.format(author.name), value='```\n' + ' '.join(args) + '\n```')
            embed.set_footer(text=author.id)
            if message.attachments:
                attachment_links = ''
                for attachment in message.attachments:
                    attachment_links += '\n' + attachment.url
                embed.add_field(name='Attachment', value=attachment_links)
            owner = discord.utils.find(lambda usr: usr.id == permitted_id[0], ev.bot.get_all_members())
            await ev.bot.send_message(owner, None, embed=embed)
