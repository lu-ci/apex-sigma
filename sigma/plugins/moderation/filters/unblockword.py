import discord
from sigma.core.permission import check_man_msg


async def unblockword(cmd, message, args):
    if not check_man_msg(message.author, message.channel):
        response = discord.Embed(title='⛔ Unpermitted. Requires Manage Messages Permission.', color=0xDB0000)
    else:
        try:
            blacklist = cmd.db.get_settings(message.guild.id, 'BlockedWords')
        except:
            cmd.db.set_settings(message.guild.id, 'BlockedWords', [])
            blacklist = []
        removed = []
        failed = []
        for word in args:
            word = word.lower()
            if word not in blacklist:
                reason = 'Not found in blacklist.'
                failed.append([word, reason])
            else:
                removed.append(word)
                blacklist.remove(word)
        cmd.db.set_settings(message.guild.id, 'BlockedWords', blacklist)
        response = discord.Embed(color=0x66CC66, title='✅ Blacklist Removals Finished')
        if removed:
            response.add_field(name='Successfull Removals', value=f'```\n{", ".join(removed)}\n```', inline=False)
        if failed:
            fail_text = ''
            for failure in failed:
                fail_text += f'\n{failure[0]} - {failure[1]}'
            response.add_field(name='Failed Removals', value=f'```\n{fail_text}\n```', inline=False)
    await message.channel.send(embed=response)
