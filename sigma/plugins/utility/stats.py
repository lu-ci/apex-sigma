from sigma.core.stats import stats as sigma_stats
from sigma.core.formatting import codeblock
import discord


async def stats(cmd, message, args):
    sigma_avatar = cmd.bot.user.avatar_url
    out = sigma_stats(cmd.bot)
    embed = discord.Embed(color=0x1abc9c)
    embed.set_author(name='Apex Sigma', url='https://auroraproject.xyz/', icon_url=sigma_avatar)
    out_txt = codeblock('\n'.join(out), syntax='haskell')
    embed.add_field(name='Stats', value=out_txt)
    await cmd.bot.send_message(message.channel, None, embed=embed)
