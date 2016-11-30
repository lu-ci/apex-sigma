from .github_control import search, linkctl, webserverctl


async def github(cmd, message, args):
    if not args:
        await cmd.bot.send_message(message.channel, cmd.help())
        return

    subcmd = args.pop(0)

    if subcmd == 'search':
        await search(message, args)
    elif subcmd == 'link':
        await linkctl(message, args)
    elif subcmd == 'websrv':
        await webserverctl(message, args)
    else:
        await cmd.bot.send_message(message.channel, cmd.help())
