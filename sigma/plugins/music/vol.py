import discord
from .music_controller import get_player, set_volume


async def vol(cmd, message, args):
    if not message.author.voice_channel:
        embed = discord.Embed(
            title=':warning: I don\'t see you in a voice channel', color=0xFF9900)
        await cmd.bot.send_message(message.channel, None, embed=embed)
        return
    player = get_player(message.server)
    if not player:
        embed = discord.Embed(
            title=':warning: No player instance currently exists', color=0xFF9900)
        await cmd.bot.send_message(message.channel, None, embed=embed)
        return
    curr_volume = player.volume
    if not args:
        embed = discord.Embed(
            title=':information_source: Current Volume: ' + str(curr_volume * 100) + '%', color=0x0099FF)
        await cmd.bot.send_message(message.channel, None, embed=embed)
        return
    try:
        new_vol = int(args[0]) / 100
    except:
        embed = discord.Embed(
            title=':exclamation: Invalid volume input', color=0xDB0000)
        await cmd.bot.send_message(message.channel, None, embed=embed)
        return
    player.volume = new_vol
    set_volume(message.server, new_vol)
    embed = discord.Embed(
        title=':white_check_mark: Volume Updated', color=0x66CC66)
    embed.add_field(name='From', value='```\n' + str(curr_volume * 100)[:-2] + '%\n```')
    embed.add_field(name='To', value='```\n' + str(player.volume * 100)[:-2] + '%\n```')
    await cmd.bot.send_message(message.channel, None, embed=embed)
