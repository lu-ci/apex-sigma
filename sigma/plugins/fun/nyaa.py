import requests
import discord
import lxml.html as l


async def nyaa(cmd, message, args):
    cmd.db.add_stats('NekoCount')

    url = 'http://artwork.nekomimi.nexus-digital.us/random'
    redirect = requests.head(url, allow_redirects=True).headers['Link'][1:]
    redirect = redirect[:redirect.find('>')]
    nyaa = requests.get(redirect)

    root = l.fromstring(nyaa.text)
    elements = root.cssselect('#posts .post-wrapper div a img')
    image = elements[0].attrib['src']
    embed = discord.Embed(color=0xff6699)
    embed.set_image(url=image)
    await cmd.bot.send_message(message.channel, None, embed=embed)
