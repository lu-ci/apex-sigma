import discord
from sigma.core.permission import check_admin


async def greet(cmd, message, args):
    if not check_admin(message.author, message.channel):
        embed = discord.Embed(title=':no_entry: Unpermitted. Server Admin Only.', color=0xDB0000)
    else:
        active = cmd.db.get_settings(message.server.id, 'Greet')
        greet_channel = cmd.db.get_settings(message.server.id, 'GreetChannel')
        if not greet_channel:
            greet_channel = message.server.default_channel.id
        if not active:
            cmd.db.set_settings(message.server.id, 'Greet', True)
            cmd.db.set_settings(message.server.id, 'GreetChannel', message.channel.id)
            embed = discord.Embed(color=0x66CC66,
                                  title=':white_check_mark: Greet Messages Enabled On ' + message.channel.name)
        else:
            if message.channel.id == greet_channel:
                cmd.db.set_settings(message.server.id, 'Greet', False)
                embed = discord.Embed(color=0x66CC66,
                                      title=':white_check_mark: Greet Messages Disabled')
            else:
                cmd.db.set_settings(message.server.id, 'GreetChannel', message.channel.id)
                embed = discord.Embed(color=0x66CC66,
                                      title=':white_check_mark: Greet Message Channel Changed To ' + message.channel.name)
    await cmd.bot.send_message(message.channel, None, embed=embed)
