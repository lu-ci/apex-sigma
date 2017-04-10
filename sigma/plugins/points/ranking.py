import discord
from config import MainServerURL


async def ranking(cmd, message, args):
    embed = discord.Embed(color=0x1ABC9C)
    embed.add_field(name='Sigma Ranking for ' + message.server.name,
                    value='You can click [HERE](' + MainServerURL + 'ranking?sid=' + message.server.id + ') to see the Sigma Ranking for this server.')
    await message.channel.send(None, embed=embed)
