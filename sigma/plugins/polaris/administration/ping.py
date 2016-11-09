import subprocess
import asyncio
from config import permitted_id


async def ping(cmd, message, args):
    if message.author.id in permitted_id:
        address = 'google.com'
        if args:
            address = args[0]
        out_text = ''
        p = subprocess.Popen(['ping.exe', address], stdout=subprocess.PIPE)
        out_text += str(p.communicate()[0]).replace('\\r', '\r').replace('\\n', '\n')[2:-1]
        await cmd.bot.send_message(message.channel, '```haskell\n' + out_text + '\n```')
    else:
        response = await cmd.bot.send_message(message.channel, 'Permitted ID Only :x:')
        await asyncio.sleep(10)
        await cmd.bot.delete_message(response)
