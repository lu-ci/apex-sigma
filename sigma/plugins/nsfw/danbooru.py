import requests
import random
import discord


async def danbooru(cmd, message, args):
    if not args:
        tag = 'nude'
    else:
        tag = ' '.join(args)
        tag = tag.replace(' ', '+')
    resource = 'https://danbooru.donmai.us/post/index.json?&tags=' + tag
    file_url_base = 'https://danbooru.donmai.us'
    data = requests.get(resource).json()
    links = []
    for post in data:
        try:
            links.append(post['file_url'])
        except:
            pass
    if len(links) == 0:
        embed = discord.Embed(color=0x696969, title=':mag: Search for ' + tag + ' yielded no results.')
        embed.set_footer(
            text='Remember to replace spaces in tags with an underscore, as a space separates multiple tags')
        await cmd.bot.send_message(message.channel, None, embed=embed)
        return
    chosen_post = random.choice(links)
    url = file_url_base + chosen_post
    embed = discord.Embed(color=0x9933FF)
    embed.set_image(url=url)
    await cmd.bot.send_message(message.channel, None, embed=embed)
