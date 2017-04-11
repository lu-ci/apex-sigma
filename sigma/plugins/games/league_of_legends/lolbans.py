import lxml.html as l
import aiohttp
from humanfriendly.tables import format_pretty_table as boop


async def lolbans(cmd, message, args):
    try:
        url = 'http://www.bestbans.com/'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as data:
                page = await data.text()
        root = l.fromstring(page)
        tiers = root.cssselect('.tier-row')[:-1]
        tier_list = []
        out_list = []
        for tier in tiers:
            header = tier.cssselect('.tier-header div h2')[0].text.strip()
            header = header[4:-5]
            tier_list.append(header)
            bans = tier.cssselect('.tier-body .col-xs-3')
            row = [header]
            for ban in bans:
                champion = ban.cssselect('.index-champ-name b')[1].text.strip()
                row.append('\"' + champion + '\"')
            out_list.append(row)
        out = boop(out_list)
        await message.channel.send('```haskell\n' + out + '\n```')
    except Exception as e:
        cmd.log.error(e)
        await message.channel.send('There was an error parsing the page.\n' + str(e))


