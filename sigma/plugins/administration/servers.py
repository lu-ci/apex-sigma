import asyncio
from humanfriendly.tables import format_pretty_table
from config import permitted_id


async def servers(cmd, message, args):
    if message.author.id in permitted_id:
        serv_lst = []
        column_lst = ['Server Name', 'Server ID', 'Members']
        for server in cmd.bot.servers:
            temp_lst = []
            n = len(server.members)
            temp_lst.append(str(server))
            temp_lst.append(str(server.id))
            temp_lst.append(str(n))
            serv_lst.append(temp_lst)
        server_list = format_pretty_table(serv_lst, column_lst)
        out_text = 'List of servers:\n```'
        out_text += server_list
        if len(out_text) > 1950:
            out_text = out_text[:1950]
            out_text += '...'
        out_text += '\n```'
        await cmd.bot.send_message(message.channel, out_text)
    else:
        error_msg = await cmd.bot.send_message(message.channel, 'Insufficient permissions.')
        await asyncio.sleep(5)
        await cmd.bot.delete_message(error_msg)
        await cmd.bot.delete_message(message)
