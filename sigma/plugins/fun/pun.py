import aiohttp
import discord


async def pun(cmd, message, args):
    cmd.db.add_stats('CancerCount')
    pun_url = 'http://www.punoftheday.com/cgi-bin/arandompun.pl'
    async with aiohttp.ClientSession() as session:
        async with session.get(pun_url) as data:
            pun_req = await data.text()
    pun_text = (str(pun_req)[len('b\'document.write(\\\'&quot;'):-len(
        '&quot;<br />\\\')\ndocument.write(\\\'<i>&copy; 1996-2016 <a href="http://www.punoftheday.com">Pun of the Day.com</a></i><br />\\\')\\n\'') - 1]).replace(
        '&rsquo;', '\'')
    embed = discord.Embed(color=0x1abc9c)
    embed.add_field(name='😒 Have A Pun', value='```\n' + pun_text + '\n```')
    await cmd.bot.send_message(message.channel, None, embed=embed)
