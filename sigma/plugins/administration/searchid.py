from config import permitted_id


async def searchid(cmd, message, args):
    if message.author.id in permitted_id:
        if not args:
            cmd.bot.send_message(message.channel, cmd.help())
            return
        else:
            search_id = args[0]
        out = '```haskell'
        for server in cmd.bot.servers:
            for user in server.members:
                if user.id == search_id:
                    out += '\nUser ' + user.name + '#' + user.discriminator + ' [' + user.id + ']' + ' has been found on ' + server.name + ' [' + server.id + '].'
        out += '\n```'
        await cmd.bot.send_message(message.channel, out)
