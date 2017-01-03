from config import Prefix

async def cmd_count_filler(ev, message, args):
    if message.content.startswith(Prefix):
        ev.db.add_stats('CMDCount')
