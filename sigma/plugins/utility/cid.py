import discord


async def cid(cmd, message, args):
    chn_id = message.channel.id
    name = 'None'
    if args:
        arguments = ' '.join(args)
        if arguments.startswith('<#'):
            chn_id = arguments[2:-1]
    for channel in message.server.channels:
        if channel.id == chn_id:
            name = channel.name
    embed = discord.Embed(color=0x0099FF)
    embed.add_field(name=':information_source: #' + name, value='`' + chn_id + '`')
    await cmd.bot.send_message(message.channel, None, embed=embed)
