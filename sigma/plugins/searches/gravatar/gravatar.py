import hashlib
import discord


async def gravatar(cmd, message, args):
    try:
        await message.delete()
    except:
        cmd.log.error('Couldn\'t delete the gravatar image calling message.')
        pass
    if args:
        email = args[0]
        email = email.encode('utf-8')
        gravatar_url = "https://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest()
        embed = discord.Embed(color=message.author.color)
        embed.set_image(url=gravatar_url)
        await message.channel.send(None, embed=embed)
    else:
        await message.channel.send(cmd.help())
        return
