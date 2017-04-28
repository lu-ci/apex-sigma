import discord


async def avatar(cmd, message, args):
    if message.mentions:
        target = message.mentions[0]
    else:
        target = message.author
    ava_url = target.avatar_url
    embed = discord.Embed(color=target.color)
    embed.set_image(url=ava_url)
    await message.channel.send(None, embed=embed)
