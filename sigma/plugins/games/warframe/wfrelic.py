import discord
import aiohttp
import lxml.html as l

relic_images = {
    'lith': 'http://vignette1.wikia.nocookie.net/warframe/images/a/ae/VoidProjectionsIronD.png/revision/latest/scale-to-width-down/160?cb=20160709035804',
    'meso': 'http://vignette1.wikia.nocookie.net/warframe/images/1/12/VoidProjectionsBronzeD.png/revision/latest/scale-to-width-down/160?cb=20160709035928',
    'neo': 'http://vignette3.wikia.nocookie.net/warframe/images/c/c5/VoidProjectionsSilverD.png/revision/latest/scale-to-width-down/160?cb=20160709035717',
    'axi': 'http://vignette2.wikia.nocookie.net/warframe/images/0/0e/VoidProjectionsGoldD.png/revision/latest/scale-to-width-down/160?cb=20160709035734'
}


async def wfrelic(cmd, message, args):
    if args:
        if len(args) == 2:
            relic_tier = args[0].upper()
            relic_type = args[1].upper()
            relic_url = 'http://warframe.wikia.com/wiki/Void_Relic'
            async with aiohttp.ClientSession() as session:
                async with session.get(relic_url) as data:
                    page = await data.text()
            root = l.fromstring(page)
            table = root.cssselect('.article-table')
            my_table = table[12]
            parts_list = ''
            for row in my_table:
                if len(row) == 4:
                    part = row[0].text
                    tier = row[1].text
                    rl_type = row[2].text
                    odds = row[3].text.strip('\n')
                    if tier == relic_tier:
                        if rl_type == relic_type:
                            parts_list += f'\n{part.title()} ({odds.title()[:1]})'
            if parts_list != '':
                embed = discord.Embed(color=0x0066CC)
                embed.set_thumbnail(url=relic_images[relic_tier.lower()])
                embed.add_field(name=f'{relic_tier.title()} {relic_type}', value=f'```\n{parts_list}\n```', inline=False)
            else:
                embed = discord.Embed(color=0x696969, title=':mag: Nothing Found')
            await cmd.bot.send_message(message.channel, None, embed=embed)
