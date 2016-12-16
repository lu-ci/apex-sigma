from sigma.core.stats import stats as sigma_stats
from sigma.core.formatting import codeblock

async def stats(cmd, message, args):
    out = sigma_stats(cmd.bot)
    out_txt = codeblock('\n'.join(out), syntax='haskell')
    await cmd.bot.send_message(message.channel, out_txt)
