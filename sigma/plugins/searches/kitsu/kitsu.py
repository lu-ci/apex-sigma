import aiohttp
import discord
import json


async def kitsu(cmd, message, args):
    if args:
        qry = '%20'.join(args)
        url = 'https://kitsu.io/api/edge/anime?filter[text]=' + qry
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as data:
                data = await data.read()
                data = json.loads(data)
        ani_url = data['data'][0]['links']['self']
        async with aiohttp.ClientSession() as session:
            async with session.get(ani_url) as data:
                data = await data.read()
                data = json.loads(data)
                data = data['data']
        attr = data['attributes']
        slug = attr['slug']
        synopsis = attr['synopsis']
        en_title = attr['titles']['en_jp']
        jp_title = attr['titles']['ja_jp']
        try:
            rating = attr['averageRating'][:5]
        except:
            rating = 'None'
        episode_count = attr['episodeCount']
        episode_length = attr['episodeLength']
        start_date = attr['startDate']
        end_date = attr['endDate']

        nsfw = attr['nsfw']
        if nsfw:
            nsfw = 'Yes'
        else:
            nsfw = 'No'
        embed = discord.Embed(color=0xff3300)
        embed.set_author(name='Kitsu.io', icon_url='https://avatars3.githubusercontent.com/u/7648832?v=3&s=200',
                         url=f'https://kitsu.io/anime/{slug}')
        embed.add_field(name='Title', value=f'```\n{en_title} [{jp_title}]\n```', inline=False)
        embed.add_field(name='Rating', value=f'```\n{rating}%\n```', inline=True)
        embed.add_field(name='NSFW', value=f'```\n{nsfw}\n```', inline=True)
        embed.add_field(name='Start Date', value=f'```\n{start_date}\n```')
        embed.add_field(name='End Date', value=f'```\n{end_date}\n```')
        embed.add_field(name='Episodes', value=f'```\n{episode_count}\n```')
        embed.add_field(name='Length', value=f'```\n{episode_length}m\n```')
        embed.add_field(name='Synopsis', value=f'```\n{synopsis[:256]}...\n```', inline=False)
        if attr['coverImage']:
            cover_image = attr['coverImage']['original'].split('?')[0]
            embed.set_image(url=cover_image)
        if attr['posterImage']:
            poster_image = attr['posterImage']['original'].split('?')[0]
            embed.set_thumbnail(url=poster_image)
        embed.set_footer(text='Click the Kitsu.io at the top to see the page of the anime.')
        await message.channel.send(None, embed=embed)
