import requests
import discord
from config import LastFMAPIKey


async def lastfm(cmd, message, args):
    lfm_user = ' '.join(args)
    lfm_url = 'http://ws.audioscrobbler.com/2.0/?method=user.gettoptracks&user=' + lfm_user + '&api_key=' + LastFMAPIKey + '&format=json'
    lfm_data = requests.get(lfm_url).json()
    embed = discord.Embed(color=0x1abc9c)
    songs_text = ''
    for i in range(0, 5):
        name = lfm_data['toptracks']['track'][i]['name']
        artist = lfm_data['toptracks']['track'][i]['artist']['name']
        songs_text += '\n\"' + name + '\" by \"' + artist + '\"'
    if songs_text == '':
        songs_text = 'None'
    embed.add_field(name='🎵 Top Songs Listened To By ' + lfm_user, value='```yaml\n' + songs_text + '\n```', inline=False)
    await cmd.bot.send_message(message.channel, None, embed=embed)
