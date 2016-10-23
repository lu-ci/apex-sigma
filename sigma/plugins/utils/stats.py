from sigma.core.stats import stats as sigma_stats
from sigma.core.formatting import codeblock
import asyncio

async def stats(cmd, message, args):
    out = sigma_stats(cmd.bot)

    out_txt = codeblock('\n'.join(out), syntax='python')

    stats_msg = await cmd.reply(out_txt)
    await asyncio.sleep(60)
    try:
        await cmd.delete_call_message()
    except Exception as e:
        cmd.log.error(e)
    try:
        await cmd.bot.delete_message(stats_msg)
    except Exception as e:
        cmd.log.error(e)
