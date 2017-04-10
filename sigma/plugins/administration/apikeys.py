import config
import discord
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
        await message.author.send(out_text)
        status = discord.Embed(type='rich', color=0x66cc66,
                                   title='✅ The API Key List has been sent to your DM.')
    else:
        status = discord.Embed(type='rich', color=0xDB0000,
                               title='⛔ Insufficient Permissions. Bot Owner Only.')
    await message.channel.send(None, embed=status)
