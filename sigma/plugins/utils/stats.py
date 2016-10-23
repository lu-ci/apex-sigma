from sigma.core.stats import stats as sigma_stats
from sigma.core.formatting import codeblock


async def stats(cmd, message, args):
    out = sigma_stats(cmd.bot)

    out_txt = codeblock('\n'.join(out), syntax='python')

    await cmd.reply(out_txt)
