import discord


async def ranking(cmd, message, args):
    embed = discord.Embed(color=0x1ABC9C)
    embed.add_field(name='Sigma Ranking for ' + message.server.name,
                    value='You can click [HERE](https://auroraproject.xyz/ranking?sid=' + message.server.id + ') to see the Sigma Ranking for this server.')
    await cmd.bot.send_message(message.channel, None, embed=embed)
