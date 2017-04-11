import aiohttp
import discord
import json


async def kitsuuser(cmd, message, args):
    if args:
        qry = '%20'.join(args)
        url = 'https://kitsu.io/api/edge/users?filter[name]=' + qry
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as data:
                data = await data.read()
                data = json.loads(data)
        profile_url = data['data'][0]['links']['self']
        async with aiohttp.ClientSession() as session:
            async with session.get(profile_url) as data:
                data = await data.read()
                data = json.loads(data)
                data = data['data']
        attr = data['attributes']
        name = attr['name']
        avatar = attr['avatar']
        bio = attr['bio']
        about = attr['about']
        life_wasted = attr['lifeSpentOnAnime']
        library_url = data['relationships']['libraryEntries']['links']['self']
        if avatar:
            avatar = avatar['original'].split('?')[0]
        else:
            avatar = 'https://avatars3.githubusercontent.com/u/7648832?v=3'
        cover = attr['coverImage']
        if cover:
            cover = cover['original'].split('?')[0]
        significant_other = attr['waifuOrHusbando']
        so_url = data['relationships'][significant_other.lower()]['links']['related']
        async with aiohttp.ClientSession() as session:
            async with session.get(so_url) as data:
                    wf_data = await data.read()
                    wf_data = json.loads(wf_data)
        if wf_data['data']:
            wf_attr = wf_data['data']['attributes']
            wf_name = wf_attr['name']
        else:
            significant_other = 'None'
            wf_name = 'Forever Alone'
        async with aiohttp.ClientSession() as session:
            async with session.get(library_url) as data:
                    lib_data = await data.read()
                    lib_data = json.loads(lib_data)
                    lib_data = lib_data['data']
        library = len(lib_data)
        embed = discord.Embed(color=0xff3300)
        embed.set_author(name=name, icon_url=avatar, url=f'https://kitsu.io/users/{name}')
        embed.add_field(name='About', value=f'```\n{about}\n```', inline=False)
        embed.add_field(name='Significant Other', value=f'```\n{significant_other}: {wf_name}\n```', inline=False)
        embed.add_field(name='Library', value=f'```\n{library}\n```', inline=True)
        embed.add_field(name='Life Wasted', value=f'```\n{life_wasted}\n```', inline=True)
        embed.add_field(name='Biography', value=f'```\n{bio}\n```', inline=False)
        if cover:
            embed.set_image(url=cover)
        embed.set_footer(text='Click the Kitsu.io at the top to see the profile of the user.')
        await message.channel.send(None, embed=embed)
