import discord
from config import permitted_id, Prefix
from sigma.core.utils import user_avatar


async def pmredirect(ev, message, args):
    cid = ev.bot.user.id
    author = message.author
    if not message.server:
        if author.id == cid or author.id in permitted_id:
            return
        else:
            if not message.content.startswith(Prefix) and author.id not in permitted_id:
                pm_response = discord.Embed(color=0x0099FF, title=f'ℹ Type `{Prefix}help` for info on how to use me!')
                await ev.bot.send_message(message.channel, None, embed=pm_response)
            ev.log.info(f'User {author.name} [{author.id}] sent a private message.')
            embed = discord.Embed(color=0x0099FF)
            if args and not ''.join(args) == '':
                embed.add_field(name='Message',
                                value='```\n' + ' '.join(args) + '\n```', inline=False)
            embed.set_footer(text=f'UserID: {author.id}')
            embed.set_author(name=f'{author.name}#{author.discriminator}', icon_url=user_avatar(author))
            if message.attachments:
                attachment_links = ''
                for attachment in message.attachments:
                    attachment_links += '\n' + attachment['url']
                embed.add_field(name='Attachments', value=attachment_links, inline=False)
            owner = discord.utils.find(lambda usr: usr.id == permitted_id[0], ev.bot.get_all_members())
            await ev.bot.send_message(owner, None, embed=embed)
