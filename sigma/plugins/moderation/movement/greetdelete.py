import discord
from sigma.core.permission import check_admin


async def greetdelete(cmd, message, args):
    if not check_admin(message.author, message.channel):
        response = discord.Embed(title='⛔ Unpermitted. Server Admin Only.', color=0xDB0000)
    else:
        try:
            del_greet = cmd.db.get_settings(message.guild.id, 'GreetDelete')
        except:
            del_greet = False
        if del_greet:
            enabled = False
            response_title = 'disabled'
        else:
            enabled = True
            response_title = 'enabled'
        cmd.db.set_settings(message.guild.id, 'GreetDelete', enabled)
        response = discord.Embed(color=0x66CC66, title=f'Greeting message deletion {response_title}')
    await message.channel.send(embed=response)
