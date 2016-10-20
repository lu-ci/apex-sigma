import asyncio

from config import permitted_id


async def servers(cmd, message, args):
    if message.author.id in permitted_id:
        out_text = 'List of servers:\n```python'

        for server in cmd.bot.servers:
            out_text += '\n\"' + str(server) + '\" (' + str(server.id) + ')'

        if len(out_text) > 1950:
            out_text = out_text[:1950]
            out_text += '...'

        out_text += '\n```'
        await cmd.reply(out_text)
    else:
        error_msg = await cmd.reply('Insufficient permissions.')
        await asyncio.sleep(5)
        await cmd.bot.delete_message(error_msg)
