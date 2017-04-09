import asyncio
from config import UseCachet


async def server_number_reporter(ev):
    if UseCachet:
        while True:
            await ev.bot.cachet_stat_up(5, len(ev.bot.servers))
            await asyncio.sleep(20)
