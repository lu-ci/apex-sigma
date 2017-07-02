import discord
import secrets

async def smitten(cmd, message, args):
    dan_id = 285232223127601152
    dawn_id = 222234484064518156
    if message.author.id == dan_id:
        target_id = dawn_id
    elif message.author.id == dawn_id:
        target_id = dan_id
    else:
        return
    target = discord.utils.find(lambda x: x.id == target_id, cmd.bot.get_all_members())
    if target:
        url_list = [
            'https://i.imgur.com/HQHsDOY.gif',
            'https://i.imgur.com/Kj9x7Az.gif'
        ]
        img_url = secrets.choice(url_list)
        response = discord.Embed(color=0xff6699, title='💝 Dan x Dawn')
        response.set_image(url=img_url)
        await target.send(embed=response)
