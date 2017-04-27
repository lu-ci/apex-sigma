import discord
from sigma.core.permission import check_admin


async def greetpm(cmd, message, args):
    if not check_admin(message.author, message.channel):
        out_content = discord.Embed(type='rich', color=0xDB0000,
                                    title='⛔ Insufficient Permissions. Server Admin Only.')
        await message.channel.send(None, embed=out_content)
    else:
        active = cmd.db.get_settings(message.guild.id, 'GreetPM')
        if active:
            cmd.db.set_settings(message.guild.id, 'GreetPM', False)
            out_content = discord.Embed(color=0x33CC33)
            out_content.add_field(name='✅ Success',
                                  value='Greeting via private message has been disabled.')
            await message.channel.send(None, embed=out_content)
        else:
            cmd.db.set_settings(message.guild.id, 'GreetPM', True)
            out_content = discord.Embed(color=0x33CC33)
            out_content.add_field(name='✅ Success',
                                  value='Greeting via private message has been enabled.')
            await message.channel.send(None, embed=out_content)
