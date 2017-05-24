import aiohttp
import random
import discord
from lxml import html

links = []
embed_titles = ['Nyaa~', 'Nyanpasu!', 'Mnya :3', 'Meow~', '(｡･ω･｡)', 'ὃ⍜ὅ', 'ㅇㅅㅇ',
                'චᆽච', 'ऴिाी', '(ФДФ)', '（ΦωΦ）', '(ꀄꀾꀄ)', 'ฅ•ω•ฅ', '⋆ටᆼට⋆', '(ꅈꇅꅈ)',
                '<ΦωΦ>', '（ФоФ)', '(^人^)', '(ꀂǒꀂ)', '(・∀・)', '(ꃪꄳꃪ)', '=ටᆼට=',
                '(ΦεΦ)', 'ʘ̥ꀾʘ̥', '(ΦёΦ)', '=ộ⍛ộ=', '(Ф∀Ф)', '(ↀДↀ)', '(Φ_Φ)', '^ↀᴥↀ^',
                'โ๏∀๏ใ', '(Φ∇Φ)', '[ΦωΦ]', '(ΦωΦ)', 'ミ๏ｖ๏彡', '(ΦзΦ)', '|ΦωΦ|',
                '(⌯⊙⍛⊙)', 'ि०॰०ॢी', '=^∇^*=', '(⁎˃ᆺ˂)', '(ㅇㅅㅇ❀)', '(ノω<。)',
                '(ↀДↀ)✧', 'ि०॰͡०ी', 'ฅ(≚ᄌ≚)', '(=･ｪ･=?', '(^･ｪ･^)', '(≚ᄌ≚)ƶƵ',
                '(○｀ω´○)', '(●ↀωↀ●)', '(｡･ω･｡)', '(*Φ皿Φ*)', '§ꊘ⃑٥ꊘ⃐§', ']*ΦωΦ)ノ']


async def fill_links():
    for x in range(0, 20):
        resource = f'http://safebooru.org/index.php?page=dapi&s=post&q=index&tags=cat_ears&pid={x}'
        async with aiohttp.ClientSession() as session:
            async with session.get(resource) as data:
                data = await data.read()
        posts = html.fromstring(data)
        for post in posts:
            if 'file_url' in post.attrib:
                file_url = post.attrib['file_url']
                extention = file_url.split('.')[-1]
                if extention in ['png', 'jpg', 'jpeg', 'gif']:
                    height = int(post.attrib['height'])
                    width = int(post.attrib['width'])
                    if width < 2000 and height < 2000:
                        links.append(post)


async def nyaa(cmd, message, args):
    if not links:
        filler_message = discord.Embed(color=0xff6699, title='🐱 One moment, filling Sigma with catgirls...')
        fill_notify = await message.channel.send(embed=filler_message)
        await fill_links()
        filler_done = discord.Embed(color=0xff6699, title=f'🐱 We added {len(links)} catgirls!')
        await fill_notify.edit(embed=filler_done)
    random.shuffle(links)
    post_choice = links.pop()
    image_url = post_choice.attrib['file_url']
    image_source = f'http://safebooru.org/index.php?page=post&s=view&id={post_choice.attrib["id"]}'
    if image_url.startswith('//'):
        image_url = 'https:' + image_url
    embed = discord.Embed(color=0xff6699)
    icon_url = 'http://3.bp.blogspot.com/_SUox58HNUCI/SxtiKLuB7VI/AAAAAAAAA08/s_st-jZnavI/s400/Azunyan+fish.jpg'
    embed.set_author(name=random.choice(embed_titles), icon_url=icon_url, url=image_source)
    embed.set_image(url=image_url)
    await message.channel.send(None, embed=embed)
