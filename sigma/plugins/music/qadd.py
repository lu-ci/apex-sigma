import discord
from .music_controller import get_queue, add_to_queue
from .yt_search import search_youtube


async def qadd(cmd, message, args):
    current_queue = get_queue(message.server)
    queue_amount = len(current_queue)
    requester = message.author.name + message.author.discriminator
    qry = ' '.join(args)
    video_url, video_id, video_title = search_youtube(qry)
    add_to_queue(message.server, requester, 'YouTube', video_url)
    embed = discord.Embed(title=':white_check_mark: Added To Queue', color=0x66CC66)
    embed.add_field(name='Title', value='**' + video_title + '**', inline=False)
    embed.add_field(name='YT Link', value='[' + video_url + '](' + video_url + ')', inline=False)
    embed.set_footer(text='Position #' + str(queue_amount + 1) + ' in queue, queued by ' + requester + '.')
    await cmd.bot.send_message(message.channel, None, embed=embed)
