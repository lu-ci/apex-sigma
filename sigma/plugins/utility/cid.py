import discord


async def cid(cmd, message, args):
    chn_id = message.channel.id
    name = 'None'
    if args:
        arguments = ' '.join(args)
        if arguments.startswith('<#'):
            chn_id = arguments[2:-1]
    for channel in message.guild.channels:
        if channel.id == chn_id:
            name = channel.name
    embed = discord.Embed(color=0x0099FF)
    embed.add_field(name='ℹ #' + name, value=f'`{chn_id}`')
    await message.channel.send(None, embed=embed)
