from config import permitted_id
import asyncio


async def announce(cmd, message, args):
    if message.author.id in permitted_id:
        if args:
            n = 0
            announcement = ' '.join(args)
            for server in cmd.bot.servers:
                await cmd.bot.send_message(server.default_channel, announcement)
                n += 1
            response = await cmd.bot.send_message(message.channel, 'Announcement sent successfully to ' + str(n) + ' servers.')
            await asyncio.sleep(10)
            await cmd.bot.delete_message(response)
        else:
            await cmd.bot.send_message(message.channel, cmd.help())
            return
