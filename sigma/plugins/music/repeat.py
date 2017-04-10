import discord


async def repeat(cmd, message, args):
    if message.server.id in cmd.music.repeaters:
        cmd.music.repeaters.remove(message.server.id)
        response = discord.Embed(color=0x0099FF, title='🔁 Queue Repeat Disabled')
    else:
        cmd.music.repeaters.append(message.server.id)
        response = discord.Embed(color=0x0099FF, title='🔁 Queue Repeat Enabled')
    await message.channel.send(None, embed=response)
