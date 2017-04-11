import discord
import pafy
from .yt_search import search_youtube


async def yt(cmd, message, args):
    if not args:
        embed = discord.Embed(color=0xDB0000, title='❗ Nothing to search for.')
        await message.channel.send(None, embed=embed)
        return
    qry = ' '.join(args)
    v_url = await search_youtube(qry)
    v_tit = pafy.new(v_url).title
    await message.channel.send('`' + v_tit + '`\n' + v_url)
