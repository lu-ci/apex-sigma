import discord


async def resume(cmd, message, args):
    player = cmd.music.get_player(message.server.id)
    if player:
        if player.is_playing():
            response = discord.Embed(color=0xFF9900, title='⚠ Already Playing.')
        else:
            player.resume()
            response = discord.Embed(color=0x0099FF, title='▶ Player Resumed')
    else:
        response = discord.Embed(color=0xFF9900, title='⚠ No Player Exists.')
    await cmd.bot.send_message(message.channel, None, embed=response)
