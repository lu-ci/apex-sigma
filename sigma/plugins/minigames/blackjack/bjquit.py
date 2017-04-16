import discord
from .black_jack_backend import get_bj, del_bj


async def bjquit(cmd, message, args):
    instance_id = message.guild.id + message.author.id
    instance = get_bj(instance_id)
    if instance:
        cmd.db.add_points(message.guild, message.author, instance['Bet'] // 2)
        del_bj(instance_id)
        embed = discord.Embed(color=0xFF9900,
                              title=':fire: Too bad... Your ' + str(instance['Bet'] // 2) + ' have been refunded.')
    else:
        embed = discord.Embed(color=0xDB0000, title='❗ No active blackjack games found for you.')
    await message.channel.send(None, embed=embed)
