async def echo(cmd, message, args):
    await message.channel.send(' '.join(args))
