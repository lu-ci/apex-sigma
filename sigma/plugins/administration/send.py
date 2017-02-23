import discord


async def send(cmd, message, args):
    if args:
        mode, identifier = args[0].split(':')
        mode = mode.lower()
        text = ' '.join(args[1:])
    else:
        embed = discord.Embed(color=0xDB0000, title=':exclamation: No Arguments Given.')
        await cmd.bot.send_message(message.channel, None, embed=embed)
        return
    if mode == 'u':
        target = discord.utils.find(lambda x: x.id == identifier, cmd.bot.get_all_members())
    elif mode == 's':
        target = discord.utils.find(lambda x: x.id == identifier, cmd.bot.servers)
        target = target.default_channel
    elif mode == 'c':
        target = discord.utils.find(lambda x: x.id == identifier, cmd.bot.get_all_channels())
    else:
        embed = discord.Embed(color=0xDB0000, title=':exclamation: Invalid Arguments Given.')
        await cmd.bot.send_message(message.channel, None, embed=embed)
        return
    await cmd.bot.send_message(target, text)
    embed = discord.Embed(color=0x66CC66, title=':white_check_mark: Message Sent.')
    await cmd.bot.send_message(message.channel, None, embed=embed)
