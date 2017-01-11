import discord


async def move(cmd, message, args):
    if message.author.voice_channel:
        voice_connected = cmd.bot.is_voice_connected(message.server)
        if voice_connected:
            voice_instance = cmd.bot.voice_client_in(message.server)
            vc_name = voice_instance.channel.name
            if voice_instance.channel == message.author.voice_channel:
                embed = discord.Embed(title=':warning: I am already in ' + vc_name, color=0xFF9900)
            else:
                await voice_instance.move_to(message.author.voice_channel)
                new_vc_name = cmd.bot.voice_client_in(message.server).channel.name
                embed = discord.Embed(title=':white_check_mark: Moved from ' + vc_name + ' to ' + new_vc_name,
                                      color=0x66CC66)
        else:
            embed = discord.Embed(title=':warning: I am not in a voice channel currently', color=0xFF9900)
    else:
        embed = discord.Embed(
            title=':warning: I don\'t see you in a voice channel', color=0xFF9900)
    await cmd.bot.send_message(message.channel, None, embed=embed)
