import discord
import aiohttp
import lxml.html as l


async def osu(cmd, message, args):
    if not args:
        await message.channel.send(cmd.help())
        return
    osu_input = ' '.join(args)
    try:
        profile_url = 'https://osu.ppy.sh/u/' + osu_input
        async with aiohttp.ClientSession() as session:
            async with session.get(profile_url) as data:
                page = await data.text()
        root = l.fromstring(page)
        username = root.cssselect('.profile-username')[0].text[:-1]
    except:
        embed = discord.Embed(color=0xDB0000, title='❗ Unable to retrieve profile.')
        await message.channel.send(None, embed=embed)
        return
    user_color = str(message.author.color)[1:]
    sig_url = 'https://lemmmy.pw/osusig/sig.php?colour=hex' + user_color + '&uname=' + osu_input
    embed = discord.Embed(color=message.author.color)
    embed.set_image(url=sig_url)
    embed.set_author(name=username + '\'s osu! Profile', url=profile_url,
                     icon_url='http://w.ppy.sh/c/c9/Logo.png')
    await message.channel.send(None, embed=embed)
