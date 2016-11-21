import requests
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from io import BytesIO
import time
import os


async def music(cmd, message, args):
    if not args:
        await cmd.bot.send_message(message.channel, cmd.help())
        return
    else:
        search = ' '.join(args)
    qry_url = 'http://api.deezer.com/search/track?q=' + search
    try:
        data = requests.get(qry_url).json()
        data = data['data']
    except Exception as e:
        await cmd.bot.send_message(message.channel,
                                   'We couldn\'t parse the page. The API might be unreachable at the moment.')
        return
    else:
        if len(data) == 0:
            await cmd.bot.send_message(message.channel, 'Nothing found.')
            return
        song = data[0]
        preview = song['preview']
        title = song['title_short']
        if len(title) > 20:
            title = title[:19] + '...'
        duration = song['duration']
        duration = time.strftime('%M:%S', time.gmtime(duration))
        artist_data = song['artist']
        artist = artist_data['name']
        if len(artist) > 20:
            artist = artist[:19] + '...'
        photo = artist_data['picture_medium']
        photo = photo.replace('250x250', '128x128')
        album_data = song['album']
        album = album_data['title']
        if len(album) > 20:
            album = album[:19] + '...'
        cover = album_data['cover_medium']
        cover = cover.replace('250x250', '128x128')
        try:
            artist_photo_raw = requests.get(photo).content
            artist_photo = Image.open(BytesIO(artist_photo_raw))
            cover_art_raw = requests.get(cover).content
            cover_art = Image.open(BytesIO(cover_art_raw))
            base = Image.open(cmd.resource('img/base.png'))
            overlay = Image.open(cmd.resource('img/overlay.png'))
            base.paste(artist_photo, (0, 0))
            base.paste(cover_art, (512, 0))
            base.paste(overlay, (0, 0), overlay)
            font = ImageFont.truetype("NotoSansCJKjp-Medium.otf", 24)
            font2 = ImageFont.truetype("NotoSansCJKjp-Medium.otf", 20)

            imgdraw = ImageDraw.Draw(base)
            imgdraw.text((132, -5), artist, (255, 255, 255), font=font)
            imgdraw.text((165, 44), title, (255, 255, 255), font=font)
            imgdraw.text((261, 92), album, (255, 255, 255), font=font)
            imgdraw.text((421, 46), duration, (255, 255, 255), font=font2)

            base.save('cache/track_' + message.author.id + '.png')

            await cmd.bot.send_file(message.channel, 'cache/track_' + message.author.id + '.png')
            await cmd.bot.send_message(message.channel, 'Track Preview: <' + preview + '>')

            os.remove('cache/track_' + message.author.id + '.png')

        except Exception as e:
            cmd.log.error(e)
            await cmd.bot.send_message(message.channel, str(e).encode('utf-8'))
            return
