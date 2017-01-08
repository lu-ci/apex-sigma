import discord
import requests
import lxml.html as l


async def osu(cmd, message, args):
    if not args:
        await cmd.bot.send_message(message.channel, cmd.help())
        return
    osu_input = ' '.join(args)
    try:
        profile_url = 'https://osu.ppy.sh/u/' + osu_input
        page = requests.get(profile_url)
        root = l.fromstring(page.text)
        username = root.cssselect('.profile-username')[0].text
    except:
        embed = discord.Embed(color=0xDB0000, title=':exclamation: Unable to retrieve profile.')
        await cmd.bot.send_message(message.channel, None, embed=embed)
        return
    user_color = str(message.author.color)[1:]
    sig_url = 'https://lemmmy.pw/osusig/sig.php?colour=hex' + user_color + '&uname=' + username
    embed = discord.Embed(color=message.author.color)
    embed.set_image(url=sig_url)
    embed.set_author(name=username + '\'s osu! Profile', url=profile_url,
                     icon_url='http://w.ppy.sh/c/c9/Logo.png')
    await cmd.bot.send_message(message.channel, None, embed=embed)
