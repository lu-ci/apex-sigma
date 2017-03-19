import discord
import pafy
from .yt_search import search_youtube


async def yt(cmd, message, args):
    if not args:
        embed = discord.Embed(color=0xDB0000, title='❗ Nothing to search for.')
        await cmd.bot.send_message(message.channel, None, embed=embed)
        return
    qry = ' '.join(args)
    v_url = await search_youtube(qry)
    v_tit = pafy.new(v_url).title
    await cmd.bot.send_message(message.channel, '`' + v_tit + '`\n' + v_url)
