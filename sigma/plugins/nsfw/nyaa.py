import random
import requests
import lxml.html as l


async def nyaa(cmd, message, args):

    url = 'http://nekogirls.nexus-digital.us/random'
    redirect = requests.get(url).headers['Link'][1:]
    redirect = redirect[:redirect.find('>')]
    nyaa = requests.get(redirect)

    root = l.fromstring(nyaa.text)
    elements = root.cssselect('#posts .post-wrapper div a img')
    image = elements[0].attrib['src']

    await cmd.reply(image)
