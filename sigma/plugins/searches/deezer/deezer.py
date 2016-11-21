import requests
from humanfriendly.tables import format_pretty_table as boop


async def deezer(cmd, message, args):
    if not args:
        await cmd.bot.send_message(message.channel, cmd.help())
        return
    else:
        profile_id = args[0]
    out_data = []
    dz_prof = 'https://api.deezer.com/user/' + profile_id
    dz_url = dz_prof + '/flow?limit=20'
    try:
        data = requests.get(dz_url).json()
        data = data['data']
        prof_data = requests.get(dz_prof).json()
        name = prof_data['name']
    except Exception as e:
        cmd.log.error(e)
        await cmd.bot.send_message(message.channel, 'We couldn\'t parse the webpage, make sure the ID is proper.')
        return
    try:
        for item in data:
            try:
                title = item['title_short']
            except:
                title = 'Unknown'
            try:
                artist = item['artist']['name']
            except:
                artist = 'Unknown'
            out_data.append([artist, title])
        table = boop(out_data)
        out = 'Some of the tracks currently in **' + name + '\'s** queue:\n```\n' + table + '\n```'
    except Exception as e:
        cmd.log.error(e)
        await cmd.bot.send_message(message.channel, 'We couldn\'t parse the webpage, make sure the ID is proper.')
        return
    try:
        await cmd.bot.send_message(message.channel, out)
    except:
        await cmd.bot.send_message(message.channel, 'The message was too long.')
