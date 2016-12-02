import requests
import lxml.html as l


async def nyaa(cmd, message, args):

    url = 'http://nekogirls.nexus-digital.us/random'
    redirect = requests.head(url, allow_redirects=True).headers['Link'][1:]
    redirect = redirect[:redirect.find('>')]
    nyaa = requests.get(redirect)

    root = l.fromstring(nyaa.text)
    elements = root.cssselect('#posts .post-wrapper div a img')
    image = elements[0].attrib['src']

    find_data = {
        'Role': 'Stats'
    }
    find_res = cmd.db.find('Stats', find_data)
    count = 0
    for res in find_res:
        try:
            count = res['NekoCount']
        except:
            count = 0
    new_count = count + 1
    updatetarget = {"Role": 'Stats'}
    updatedata = {"$set": {"NekoCount": new_count}}
    cmd.db.update_one('Stats', updatetarget, updatedata)

    await cmd.bot.send_message(message.channel, image)
