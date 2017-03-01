import aiohttp
import discord
import lxml.html as l


async def nyaa(cmd, message, args):
    cmd.db.add_stats('NekoCount')

    url = 'http://artwork.nekomimi.nexus-digital.us/random'
    async with aiohttp.ClientSession() as session:
        async with session.get(url, allow_redirects=True) as redirect:
            redirect = redirect.headers.get('Link')[1:]
        redirect = redirect[:redirect.find('>')]
        async with session.get(redirect) as data:
            nyaa_data = await data.text()

    root = l.fromstring(nyaa_data)
    elements = root.cssselect('#posts .post-wrapper div a img')
    image = elements[0].attrib['src']
    embed = discord.Embed(color=0xff6699)
    embed.set_image(url=image)
    await cmd.bot.send_message(message.channel, None, embed=embed)
