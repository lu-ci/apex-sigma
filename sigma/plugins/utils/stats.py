from config import permitted_id
from config import sigma_version

from sigma.core.formatting import codeblock


async def stats(cmd, message, args):
    permed_ids = ', '.join(['[{:s}]'.format(x) for x in permitted_id])

    authors = ', '.join(['"{:s}"'.format(n) for n in cmd.bot.authors])
    contributors = ', '.join(['"{:s}"'.format(n) for n in cmd.bot.contributors])

    out_txt = 'Logged In As: {:s}\n'.format(cmd.bot.user.name)
    out_txt += 'User ID: {:s}\n'.format(cmd.bot.user.id)
    out_txt += 'Authors: {:s}\n'.format(authors)
    out_txt += 'Contributors: {:s}\n'.format(contributors)
    out_txt += 'Sigma Version: {:s}\n'.format(sigma_version)
    out_txt += 'Connected to [ {:d} ] servers.\n'.format(cmd.bot.server_count)
    out_txt += 'Serving [ {:d} ] users.\n'.format(cmd.bot.member_count)
    out_txt += 'Permitted IDs: {:s}\n'.format(permed_ids)

    await cmd.reply(codeblock(out_txt, syntax='python'))
