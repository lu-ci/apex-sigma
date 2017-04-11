import aiohttp
import discord
import json
from lxml import html

wk_base_url = 'https://www.wanikani.com/api/user/'


async def get_user_data(cmd, message, key=None, username=None):
    user = {
        'method': None,
        'name': '',
        'title': '',
        'avatar': ['', None],
        'level': 0,
        'creation_date': 0,
        'forums': {'posts': 0, 'topics': 0},
        'srs': {
            'apprentice': 0,
            'guru': 0,
            'master': 0,
            'enlightened': 0,
            'burned': 0
        },
        'radicals': {'total': 0, 'current': 0},
        'kanji': {'total': 0, 'current': 0},
        'lessons': {'now': 0},
        'reviews': {'now': 0, 'next_hour': 0, 'next_day': 0, 'next_date': 0},
    }

    srs_dist = None
    lvl_prog = None
    queue = None
    userinfo = None

    # if we have a key, pull data directly from API
    if key:
        url = wk_base_url + key

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url + '/srs-distribution') as data:
                    srs_dist = await data.json()
            async with aiohttp.ClientSession() as session:
                async with session.get(url + '/level-progression') as data:
                    lvl_prog = await data.json()
                    lvl_prog = lvl_prog['requested_information']
            async with aiohttp.ClientSession() as session:
                async with session.get(url + '/study-queue') as data:
                    queue = await data.json()
                    queue = queue['requested_information']
        except ConnectionError as e:
            cmd.bot.send_message(message.channel, 'Failed to get user data.')
            cmd.log.error('{:s}'.format(e))
            raise e

        userinfo = srs_dist['user_information']
        srs_dist = srs_dist['requested_information']

        user['method'] = 'api'
        user['radicals']['total'] = lvl_prog['radicals_total']
        user['radicals']['current'] = lvl_prog['radicals_progress']
        user['kanji']['total'] = lvl_prog['kanji_total']
        user['kanji']['current'] = lvl_prog['kanji_progress']
        user['lessons']['now'] = queue['lessons_available']
        user['reviews']['now'] = queue['reviews_available']
        user['reviews']['next_hour'] = queue['reviews_available_next_hour']
        user['reviews']['next_day'] = queue['reviews_available_next_day']
        user['reviews']['next_date'] = queue['next_review_date']

    # otherwise if we have a username, pull data from profile page
    elif username:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://www.wanikani.com/community/people/' + username) as data:
                page = await data.text()
        tree = html.fromstring(page)

        script = tree.xpath('//div[@class="footer-adjustment"]/script')
        if script != []:
            script = script[0].text.strip()
        else:
            embed = discord.Embed(color=0xDB0000,
                                  title='❗ Error while parsing the page, profile not found or doesn\'t exist')
            await message.channel.send(None, embed=embed)
            return None

        script = script[script.find('var srsCounts'): script.find(
            'Counts.fillInSrsCount(srsCounts.requested_information);')]
        script = script.strip()[16:-1]

        userinfo = json.loads(script)['user_information']
        srs_dist = json.loads(script)['requested_information']
        user['method'] = 'html'
    else:
        return None

    user['name'] = userinfo['username']
    user['title'] = userinfo['title']
    user['level'] = userinfo['level']
    user['avatar'][0] = 'https://www.gravatar.com/avatar/' + \
                        userinfo['gravatar']
    user['creation_date'] = userinfo['creation_date']
    user['forums']['posts'] = userinfo['posts_count']
    user['forums']['topics'] = userinfo['topics_count']
    user['srs']['apprentice'] = srs_dist['apprentice']['total']
    user['srs']['guru'] = srs_dist['guru']['total']
    user['srs']['master'] = srs_dist['master']['total']
    user['srs']['enlightened'] = srs_dist['enlighten']['total']
    user['srs']['burned'] = srs_dist['burned']['total']

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(user['avatar'][0]) as data:
                user['avatar'][1] = await data.read()
    except ConnectionError as e:
        cmd.bot.send_message(message.channel, 'Failed to get user avatar.')
        cmd.log.error('{:s}'.format(e))

    return user


async def get_key(cmd, message, args):
    # if no arguments passed, pulling the ID of a caller
    if not args:
        user_id = str(message.author.id)
    # otherwise see if someone was mentioned
    elif len(message.mentions) > 0:
        user_id = message.mentions[0].id
    # otherwise, pull the username out of a message
    else:
        key = None
        try:
            username = args[0]
        except Exception as e:
            cmd.log.error(e)
            embed = discord.Embed(color=0xDB0000, title='❗ Error while parsing the input message.')
            await message.channel.send(None, embed=embed)
            return

    if 'username' not in locals():
        if 'user_id' not in locals():
            embed = discord.Embed(color=0xDB0000, title='❗ No arguments passed.')
            await message.channel.send(None, embed=embed)
            return
        # a username was passed
        else:
            query = {'UserID': int(user_id)}
            search = cmd.db.find('WaniKani', query)
            db_response = None
            for result in search:
                db_response = result
            try:
                key = db_response['WKAPIKey']
                username = db_response['WKUsername']
            except:
                embed = discord.Embed(color=0xDB0000, title='❗ No Assigned Key or Username Found')
                embed.add_field(name='To Add A Key', value='Use `' + cmd.prefix + 'wksave key YOUR_API_KEY_HERE`')
                await message.channel.send(None, embed=embed)

                return (None, None)

    return (key, username)
