import aiohttp
import discord


async def wfwiki(cmd, message, args):
    if args:
        qry = ' '.join(args)
        wiki_search_url = f'http://warframe.wikia.com/api/v1/Search/List?query={qry}'
        search_params = '&limit=1&minArticleQuality=10&batch=1&namespaces=0%2C14'
        wiki_search_url += search_params
        async with aiohttp.ClientSession() as session:
            async with session.get(wiki_search_url) as data:
                search_json = await data.json()
                try:
                    article_id = search_json['items'][0]['id']
                except:
                    embed = discord.Embed(color=0x696969, title='🔍 Nothing Found')
                    await message.channel.send(None, embed=embed)
                    return
                article_url = search_json['items'][0]['url']
            article_data_url = f'http://warframe.wikia.com/api/v1/Articles/AsSimpleJson?id={article_id}'
            async with session.get(article_data_url) as article_page_data:
                article_data = await article_page_data.json()
        prim_data = article_data['sections'][0]
        art_title = prim_data['title']
        art_summ = ''
        for x in prim_data['content']:
            art_summ += '\n' + x['text']
        if len(art_summ) > 512:
            art_summ = art_summ[:512] + '...'
        embed = discord.Embed(color=0x0066CC)
        embed.add_field(name=art_title, value=f'```\n{art_summ}\n```')
        icon_url = 'http://fc08.deviantart.net/fs70/f/2013/362/8/b/warframe_icon__alternative__by_bokuwatensai-d6zs6fz.png'
        embed.set_author(name='Warframe Wikia', icon_url=icon_url, url=article_url)
        await message.channel.send(None, embed=embed)
