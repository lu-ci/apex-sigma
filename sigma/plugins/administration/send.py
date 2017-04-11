import discord


async def send(cmd, message, args):
    if args:
        mode, identifier = args[0].split(':')
        identifier = int(identifier)
        mode = mode.lower()
        text = ' '.join(args[1:])
    else:
        embed = discord.Embed(color=0xDB0000, title='❗ No Arguments Given.')
        await message.channel.send(None, embed=embed)
        return
    if mode == 'u':
        target = discord.utils.find(lambda x: x.id == identifier, cmd.bot.get_all_members())
    elif mode == 's':
        target = discord.utils.find(lambda x: x.id == identifier, cmd.bot.guilds)
        target = target.default_channel
    elif mode == 'c':
        target = discord.utils.find(lambda x: x.id == identifier, cmd.bot.get_all_channels())
    else:
        embed = discord.Embed(color=0xDB0000, title='❗ Invalid Arguments Given.')
        await message.channel.send(None, embed=embed)
        return
    await target.send(text)
    embed = discord.Embed(color=0x66CC66, title=f'✅ Message sent to {target.name}.')
    await message.channel.send(None, embed=embed)
