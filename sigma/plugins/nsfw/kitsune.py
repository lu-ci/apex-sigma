import random
import discord
from .safe_core import grab_post_list, generate_embed


links = []
embed_titles = ['Fluffy tails are supreme!']

async def kitsune(cmd, message, args):
    global links
    if not links:
        filler_message = discord.Embed(color=0xff3300, title='🦊 One moment, filling Sigma with foxes...')
        fill_notify = await message.channel.send(embed=filler_message)
        links = await grab_post_list('fox_tail')
        filler_done = discord.Embed(color=0xff3300, title=f'🦊 We added {len(links)} kitsune!')
        await fill_notify.edit(embed=filler_done)
    random.shuffle(links)
    post_choice = links.pop()
    icon = 'https://static.tvtropes.org/pmwiki/pub/images/Holo_Ears_7860.jpg'
    response = generate_embed(post_choice, embed_titles, 0xff3300, icon=icon)
    await message.channel.send(None, embed=response)
