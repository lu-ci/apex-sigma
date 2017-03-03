import asyncio


async def init_clock(music, sid):
    await asyncio.sleep(5)
    music.remove_init(sid)
