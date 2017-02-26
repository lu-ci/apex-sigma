import os
import aiohttp
import nhentai as nh
from PIL import Image
from io import BytesIO


async def nhentai(cmd, message, args):
    search = ' '.join(args)

    try:
        n = 0
        list_text = '```'

        for entry in nh.search(search)['result']:
            n += 1
            list_text += '\n#' + str(n) + ' ' + entry['title']['pretty']

        if len(nh.search(search)['result']) > 1:
            await cmd.bot.send_message(message.channel, list_text + '\n```')
            choice = await cmd.bot.wait_for_message(author=message.author, channel=message.channel, timeout=20)
            await cmd.bot.send_typing(message.channel)

            try:
                nh_no = int(choice.content) - 1
            except:
                await cmd.bot.send_message(message.channel, 'Not a number or timed out... Please start over')
                return
        else:
            nh_no = 0

        if nh_no > len(nh.search(search)['result']):
            await cmd.bot.send_message(message.channel, 'Number out of range...')
        else:
            hen_name = nh.search(search)['result'][nh_no]['title']['pretty']
            hen_id = nh.search(search)['result'][nh_no]['id']
            hen_media_id = nh.search(search)['result'][nh_no]['media_id']
            hen_url = ('https://nhentai.net/g/' + str(hen_id) + '/')
            hen_img = ('https://i.nhentai.net/galleries/' + str(hen_media_id) + '/1.jpg')
            nhen_text = ''
            async with aiohttp.ClientSession() as session:
                async with session.get(hen_img) as data:
                    nh_cover_raw = await data.read()
            nh_cover_res = Image.open(BytesIO(nh_cover_raw))
            nh_cover = nh_cover_res.resize((251, 321), Image.ANTIALIAS)

            base = Image.open(cmd.resource('img/base.png'))
            overlay = Image.open(cmd.resource('img/overlay_nh.png'))

            base.paste(nh_cover, (100, 0))
            base.paste(overlay, (0, 0), overlay)
            base.save('cache/nh_' + message.author.id + '.png')

            for tags in nh.search(search)['result'][nh_no]['tags']:
                nhen_text += '[' + str(tags['name']).title() + '] '
            await cmd.bot.send_file(message.channel, 'cache/nh_' + message.author.id + '.png')
            await cmd.bot.send_message(message.channel, 'Name:\n```\n' + hen_name + '\n```\nTags:\n```\n' + nhen_text + '\n```\nBook URL: <' + hen_url + '>')
            os.remove('cache/nh_' + message.author.id + '.png')

    except nh.nhentai.nHentaiException as e:
        await cmd.bot.send_message(message.channel, e)
