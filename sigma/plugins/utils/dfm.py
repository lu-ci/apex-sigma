import requests
import time

async def dfm(cmd, message, args):
    if not args:
        await cmd.reply(cmd.help())
        return
    else:
        genre = args[0]
        genre = genre.lower()
        dfm_url = 'https://temp.discord.fm/libraries/queue'
        data = requests.get(dfm_url).json()
        if genre.startswith('retr'):
            genre = 'retro-renegade'
        elif genre.startswith('hip'):
            genre = 'hip-hop'
        elif genre.startswith('chil'):
            genre = 'chill-corner'
        elif genre.startswith('elec'):
            genre = 'electro-hub'
        elif genre.startswith('kore'):
            genre = 'korean-madness'
        elif genre.startswith('japa'):
            genre = 'japanese-lounge'
        elif genre.startswith('rock'):
            genre = 'rock-n-roll'
        elif genre.startswith('clas'):
            genre = 'classical'
        elif genre.startswith('cof') or genre.startswith('jaz'):
            genre = 'coffee-house-jazz'
        elif genre.startswith('met'):
            genre = 'metal-mix'
        else:
            await cmd.reply('Unrecognized Discord.FM Category.')
            return

        info = data[genre]['current']
        title = info['title']
        length = info['length']
        length = time.strftime('%M:%S', time.gmtime(length))
        source = info['service']
        identifier = info['identifier']
        likes = info['social']['likes']
        views = info['social']['views']

        out_text = 'Information on the currently playing song in Discord.FM\'s ' + genre
        out_text += '\n```haskell'
        out_text += '\nTitle: ' + title
        out_text += '\nLength: ' + length
        out_text += '\nSource: ' + source
        out_text += '\nID: ' + identifier
        out_text += '\nViews: ' + views
        out_text += '\nLikes: ' + likes
        out_text += '\n```'
        await cmd.reply(out_text)
