import discord


async def osu(cmd, message, args):
    osu_input = ' '.join(args)
    user_color = str(message.author.color)[1:]
    sig_url = 'https://lemmmy.pw/osusig/sig.php?colour=hex' + user_color + '&uname=' + osu_input
    embed = discord.Embed(color=message.author.color)
    embed.set_image(url=sig_url)
    await cmd.bot.send_message(message.channel, None, embed=embed)
