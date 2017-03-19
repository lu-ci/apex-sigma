import discord
from sigma.core.permission import check_admin


async def greet(cmd, message, args):
    if not check_admin(message.author, message.channel):
        embed = discord.Embed(title='⛔ Unpermitted. Server Admin Only.', color=0xDB0000)
    else:
        active = cmd.db.get_settings(message.server.id, 'Greet')
        greet_channel = cmd.db.get_settings(message.server.id, 'GreetChannel')
        if not active:
            cmd.db.set_settings(message.server.id, 'Greet', True)
            if not greet_channel:
                cmd.db.set_settings(message.server.id, 'GreetChannel', message.server.default_channel.id)
            embed = discord.Embed(color=0x66CC66,
                                  title='✅ Greeting Messages Enabled')
        else:
            cmd.db.set_settings(message.server.id, 'Greet', False)
            embed = discord.Embed(color=0x66CC66,
                                  title='✅ Greeting Messages Disabled')
    await cmd.bot.send_message(message.channel, None, embed=embed)
