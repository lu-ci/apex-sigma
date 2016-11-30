import config
import asyncio
from config import permitted_id
from humanfriendly.tables import format_pretty_table as boop


async def apikeys(cmd, message, args):
    if message.author.id in permitted_id:
        out_list = []
        for option in dir(config):
            if not option.startswith('__'):
                option_value = getattr(config, option)
                if option_value == '':
                    option_state = '✖'
                else:
                    option_state = '✔'
                out_list.append([option.upper(), option_state])
        out_text = '```haskell\n' + boop(out_list) + '\n```'
        try:
            await cmd.bot.start_private_message(message.author)
            await cmd.bot.send_message(message.author, out_text)
        except Exception as e:
            cmd.log.error(e)
            await cmd.bot.send_message(message.channel, str(e))
        status = await cmd.bot.send_message(message.channel, 'The API Key List has been sent to your DM.')
    else:
        status = await cmd.bot.send_message(message.channel, 'Insufficient permissions. :x:')
    await asyncio.sleep(10)
    await cmd.bot.delete_message(message)
    await cmd.bot.delete_message(status)


