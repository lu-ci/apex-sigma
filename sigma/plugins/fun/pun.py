import aiohttp
import discord


async def pun(cmd, message, args):
    cmd.db.add_stats('CancerCount')
    pun_url = 'http://www.punoftheday.com/cgi-bin/arandompun.pl'
    async with aiohttp.ClientSession() as session:
        async with session.get(pun_url) as data:
            pun_req = await data.text()
    print(pun_req)
    pun_text = pun_req.split('&quot;')[1]
    embed = discord.Embed(color=0x1abc9c)
    embed.add_field(name='😒 Have A Pun', value='```\n' + pun_text + '\n```')
    await message.channel.send(None, embed=embed)
