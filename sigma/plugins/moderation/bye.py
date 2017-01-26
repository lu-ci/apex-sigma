import discord
from sigma.core.permission import check_admin


async def bye(cmd, message, args):
    if not check_admin(message.author, message.channel):
        embed = discord.Embed(title=':no_entry: Unpermitted. Server Admin Only.', color=0xDB0000)
    else:
        active = cmd.db.get_settings(message.server.id, 'Bye')
        bye_channel = cmd.db.get_settings(message.server.id, 'ByeChannel')
        if not bye_channel:
            bye_channel = message.server.default_channel.id
        if not active:
            cmd.db.set_settings(message.server.id, 'Bye', True)
            cmd.db.set_settings(message.server.id, 'ByeChannel', message.channel.id)
            embed = discord.Embed(color=0x66CC66,
                                  title=':white_check_mark: Bye Messages Enabled On ' + message.channel.name)
        else:
            if message.channel.id == bye_channel:
                cmd.db.set_settings(message.server.id, 'Bye', False)
                embed = discord.Embed(color=0x66CC66,
                                      title=':white_check_mark: Bye Messages Disabled')
            else:
                cmd.db.set_settings(message.server.id, 'ByeChannel', message.channel.id)
                embed = discord.Embed(color=0x66CC66,
                                      title=':white_check_mark: Bye Message Channel Changed To ' + message.channel.name)
    await cmd.bot.send_message(message.channel, None, embed=embed)
