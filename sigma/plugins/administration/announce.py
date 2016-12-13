from config import permitted_id
import asyncio

async def announce(cmd, message, args):
    if message.author.id in permitted_id:
        if args:
            n = 0
            announcement = ' '.join(args)
            for server in cmd.bot.servers:
                try:
                    await cmd.bot.send_message(server.default_channel, announcement)
                    n += 1
                    cmd.log.info('Sent to ' + str(server.name))
                except Exception as e:
                    cmd.log.error(e)
                    pass
                await asyncio.sleep(0.25)
            await cmd.bot.send_message(message.channel, 'Announcement sent successfully to ' + str(n) + ' servers.')
        else:
            await cmd.bot.send_message(message.channel, cmd.help())
            return
