from config import permitted_id
import asyncio


async def leave(cmd, message, args):
    if message.author.id in permitted_id:
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
    else:
        response = cmd.reply('Unpermitted :x:')
        await asyncio.sleep(10)
        await cmd.bot.delete_message(response)
