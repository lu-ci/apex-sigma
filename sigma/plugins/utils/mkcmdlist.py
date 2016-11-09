import os
import asyncio
import json

from config import permitted_id


async def mkcmdlist(cmd, message, args):
    if message.author.id in permitted_id:
        out_text = 'Command |  Description |  Usage'
        out_text += '\n--------|--------------|-------'

        try:
            os.remove('COMMANDLIST.md')
        except Exception as e:
            cmd.log.error(e)

        with open('storage/help.json', 'r', encoding='utf-8') as help_file:
            help_data = help_file.read()
            help_data = json.loads(help_data)

        for entry in help_data:
            out_text += '\n`' + cmd.prefix + entry + '`  |  ' + help_data[entry]['description'].replace('%pfx%', str(
                cmd.prefix)) + '  |  `' + help_data[entry]['usage'].replace('%pfx%', str(cmd.pfx)) + '`'

        with open("COMMANDLIST.md", "w") as text_file:
            text_file.write(out_text)

        response = await cmd.bot.send_message(message.channel, 'Done :ok_hand:')
        await asyncio.sleep(5)
        await cmd.bot.delete_message(response)
    else:
        response = await cmd.bot.reply('Unpermitted :x:')
        await asyncio.sleep(5)
        await cmd.bot.delete_message(response)
