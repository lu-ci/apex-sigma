import discord
from .music_controller import get_queue, add_to_queue
from sigma.plugins.searches.google.yt_search import search_youtube


async def queue(cmd, message, args):
    current_queue = get_queue(message.server)
    queue_amount = len(current_queue)
    if not args:
        if queue_amount == 0:
            embed = discord.Embed(color=0x0099FF, title=':information_source: The queue is empty.')
            await cmd.bot.send_message(message.channel, None, embed=embed)
            return
        queue_text = '```yaml\n'
        for item in current_queue:
            queue_text += '\n\'' + item['Title'] + '\'\n  - ' + item['Requester']
        queue_text += '\n```'
        embed = discord.Embed(color=0x0099FF)
        embed.add_field(name=':information_source: Current Queue For ' + message.server.name, value=queue_text,
                        inline=True)
        await cmd.bot.send_message(message.channel, None, embed=embed)
    else:
        requester = message.author.name + message.author.discriminator
        qry = ' '.join(args)
        video_url, video_id, video_title = search_youtube(qry)
        add_to_queue(message.server, requester, 'YouTube', video_url, video_title)
        embed = discord.Embed(title=':white_check_mark: Added To Queue', color=0x66CC66)
        embed.add_field(name='Title', value='**' + video_title + '**', inline=False)
        embed.add_field(name='YT Link', value='[' + video_url + '](' + video_url + ')', inline=False)
        embed.set_footer(text='Position #' + str(queue_amount + 1) + ' in queue, queued by ' + requester + '.')
        await cmd.bot.send_message(message.channel, None, embed=embed)
