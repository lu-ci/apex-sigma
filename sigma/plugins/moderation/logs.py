import discord
import hashlib
import random
from sigma.core.permission import check_admin


async def logs(cmd, message, args):
    if not check_admin(message.author, message.channel):
        out_content = discord.Embed(type='rich', color=0xDB0000,
                                    title=':no_entry: Insufficient Permissions. Server Admin Only.')
        await cmd.bot.send_message(message.channel, None, embed=out_content)
        return
    base_url = 'https://auroraproject.xyz/'
    admin_id = message.author.id
    server_id = message.server.id
    find_data = {
        'ServerID': server_id,
        'AdminID': admin_id
    }
    get_key = cmd.db.find_one('LogKeys', find_data)
    if get_key:
        out_content = discord.Embed(type='rich', color=0x66cc66,
                                    title=':white_check_mark: A Link Has Been Sent To You.')
        await cmd.bot.send_message(message.channel, None, embed=out_content)
        embed = discord.Embed(color=0x0099FF, title=':information_source: Log Access for ' + message.server.name,
                              url=base_url + 'server_logs?token=' + server_id + '-' + get_key['AccessKey'])
        embed.set_footer(text='All links are single use.')
        await cmd.bot.send_message(message.author, None, embed=embed)
    else:
        randomizer = random.randint(999999, 9999999999)
        string_to_encrypt = server_id + str(randomizer) + admin_id
        crypt = hashlib.md5()
        crypt.update(string_to_encrypt.encode('utf-8'))
        final = crypt.hexdigest()
        data = {
            'ServerID': server_id,
            'AdminID': admin_id,
            'AccessKey': final
        }
        cmd.db.insert_one('LogKeys', data)
        out_content = discord.Embed(type='rich', color=0x66cc66,
                                    title=':white_check_mark: A Link Has Been Sent To You.')
        await cmd.bot.send_message(message.channel, None, embed=out_content)
        embed = discord.Embed(color=0x0099FF, title=':information_source: Log Access for ' + message.server.name,
                              url=base_url + 'server_logs?token=' + server_id + '-' + final)
        embed.set_footer(text='All links are single use.')
        await cmd.bot.send_message(message.author, None, embed=embed)
