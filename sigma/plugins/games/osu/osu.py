import discord


async def osu(cmd, message, args):
    try:
        osu_input = ' '.join(args)

        sig_url = 'https://lemmmy.pw/osusig/sig.php?colour=pink&uname=' + osu_input
        embed = discord.Embed(title=osu_input.upper(), color=0xff0066)
        embed.set_image(url=sig_url)
        await cmd.bot.send_message(message.channel, None, embed=embed)
    except Exception as e:
        cmd.log.error(e)
        await cmd.bot.send_message(message.channel, 'Something went wrong or the user was not found.')
