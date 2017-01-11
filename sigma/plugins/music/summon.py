import discord
from config import Prefix


async def summon(cmd, message, args):
    voice_connected = cmd.bot.is_voice_connected(message.server)
    if message.author.voice_channel:
        if voice_connected:
            embed = discord.Embed(
                title=':warning: I am currently in ' + cmd.bot.voice_client_in(message.server).channel.name, color=0xFF9900)
            embed.add_field(name='To Move Me', value='Use `' + Prefix + 'move`')
            embed.add_field(name='To Disconnect Me', value='Use `' + Prefix + 'disconnect`')
        else:
            await cmd.bot.join_voice_channel(message.author.voice_channel)
            embed = discord.Embed(title=':white_check_mark: Joined ' + message.author.voice_channel.name, color=0x66cc66)
    else:
        embed = discord.Embed(
            title=':warning: I don\'t see you in a voice channel', color=0xFF9900)
    await cmd.bot.send_message(message.channel, None, embed=embed)
