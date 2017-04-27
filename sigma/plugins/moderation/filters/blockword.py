import discord
from sigma.core.permission import check_man_msg


async def blockword(cmd, message, args):
    if not check_man_msg(message.author, message.channel):
        response = discord.Embed(title='⛔ Unpermitted. Requires Manage Messages Permission.', color=0xDB0000)
    else:
        try:
            blacklist = cmd.db.get_settings(message.guild.id, 'BlockedWords')
        except:
            cmd.db.set_settings(message.guild.id, 'BlockedWords', [])
            blacklist = []
        added = []
        failed = []
        for word in args:
            word = word.lower()
            if word in blacklist:
                reason = 'Already in blacklist.'
                failed.append([word, reason])
            elif len(word) < 3:
                reason = 'Word too short.'
                failed.append([word, reason])
            else:
                added.append(word)
                blacklist.append(word)
        cmd.db.set_settings(message.guild.id, 'BlockedWords', blacklist)
        response = discord.Embed(color=0x66CC66, title='✅ Blacklist Addition Finished')
        if added:
            response.add_field(name='Successfull Additions', value=f'```\n{", ".join(added)}\n```', inline=False)
        if failed:
            fail_text = ''
            for failure in failed:
                fail_text += f'\n{failure[0]} - {failure[1]}'
            response.add_field(name='Failed Additions', value=f'```\n{fail_text}\n```', inline=False)
    await message.channel.send(embed=response)
