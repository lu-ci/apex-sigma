import discord
from sigma.core.permission import check_admin


async def byedelete(cmd, message, args):
    if not check_admin(message.author, message.channel):
        response = discord.Embed(title='⛔ Unpermitted. Server Admin Only.', color=0xDB0000)
    else:
        try:
            del_bye = cmd.db.get_settings(message.guild.id, 'ByeDelete')
        except:
            del_bye = False
        if del_bye:
            enabled = False
            response_title = 'disabled'
        else:
            enabled = True
            response_title = 'enabled'
        cmd.db.set_settings(message.guild.id, 'ByeDelete', enabled)
        response = discord.Embed(color=0x66CC66, title=f'Goodbye message deletion {response_title}')
    await message.channel.send(embed=response)
