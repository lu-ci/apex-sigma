import discord
from .yt_search import search_youtube


async def yt(cmd, message, args):
    if not args:
        embed = discord.Embed(color=0xDB0000, title=':exclamation: Nothing to search for.')
        await cmd.bot.send_message(message.channel, None, embed=embed)
        return
    qry = ' '.join(args)
    v_url, v_id, v_tit = search_youtube(qry)
    await cmd.bot.send_message(message.channel, '`' + v_tit + '`\n' + v_url)
