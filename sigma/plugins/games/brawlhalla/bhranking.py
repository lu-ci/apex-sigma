import discord
import aiohttp
import lxml.html as l


async def bhranking(cmd, message, args):
    regions = ['global', 'us-e', 'eu', 'sea', 'br2', 'aus', 'us-w']
    url_base = 'http://www.brawlhalla.com/rankings/1v1/'
    if not args:
        region = 'global'
    else:
        region = args[0].lower()
        if region not in regions:
            embed = discord.Embed(color=0xDB0000)
            embed.add_field(name='❗ Invalid Region',
                            value='```\nRegions: ' + ', '.join(regions).upper() + '\n```')
            await message.channel.send(None, embed=embed)
            return
    if region == 'global':
        lb_url = url_base
    else:
        lb_url = url_base + region + '/'
    async with aiohttp.ClientSession() as session:
        async with session.get(lb_url) as data:
            page = await data.text()
    root = l.fromstring(page)
    table = root.cssselect('#content')[0][0][0]
    rankings = []
    for row in table:
        if len(row) == 8:
            if row[1].text == 'Rank':
                pass
            else:
                rank_data = {
                    'Rank': row[1].text,
                    'Region': row[2].text,
                    'Name': row[3].text,
                    'WL': row[5].text,
                    'Season': row[6].text,
                    'Peak': row[7].text
                }
                rankings.append(rank_data)
    player_list = ''
    embed = discord.Embed(color=0xFF3300)
    for x in range(0, 10):
        data = rankings[x]
        out = '{:s}: {:s} | Season: {:s} | Peak: {:s}'.format(data['Region'], data['Name'],
                                                              data['Season'], data['Peak'])
        player_list += '\n' + out
    embed.add_field(name='Region', value='```\n' + region.upper() + '\n```', inline=False)
    embed.add_field(name='Brawhalla 1v1 Top 10 Ranked Players', value='```\n' + player_list + '\n```', inline=False)
    await message.channel.send(None, embed=embed)
