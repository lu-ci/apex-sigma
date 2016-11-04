async def leave(cmd, message, args):
    if not args:
        await cmd.reply(cmd.help())
    else:
        search_id = args[0]
        try:
            for server in cmd.bot.servers:
                if server.id == search_id:
                    s_name = server.name
                    await cmd.bot.leave_server(server)
                    await cmd.reply('I have left ' + s_name)
                    return
            await cmd.reply('No server with that ID has been found')
        except Exception as e:
            cmd.log.error(e)
