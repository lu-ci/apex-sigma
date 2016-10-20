from sigma.core.formatting import bold

from config import donators


async def donors(cmd, message, args):
    out_text = ''

    for donor in donators:
        out_text += '\n{:s} :ribbon: '.format(bold(donor))

    out_text += '\n'
    out_text += '\nPlease consider donating by hitting the Donate button '
    out_text += '\non this page: <https://auroraproject.xyz/donors>!'
    out_text += '\nThank you.'

    await cmd.reply(out_text)
