import discord
from sigma.core.utils import user_avatar

async def nowplaying(cmd, message, args):
    if message.server.id in cmd.music.currents:
        item = cmd.music.currents[message.server.id]
        req = item['requester']
        video = item['video']
        url = item['url']
        embed = discord.Embed(color=0x0099FF)
        embed.set_thumbnail(url=video.thumb)
        embed.set_author(name=f'{req.name}#{req.discriminator}', icon_url=user_avatar(req), url=url)
        embed.add_field(name=':information_source: Currently Playing', value=f'{video.title}')
        embed.set_footer(text=f'Duration: {video.duration} | Click the author above to go to that video.')
        await cmd.bot.send_message(message.channel, None, embed=embed)
    else:
        embed = discord.Embed(color=0x0099FF, title=':information_source: No Currently Playing Item')
        await cmd.bot.send_message(message.channel, None, embed=embed)
