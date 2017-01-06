import discord
from sigma.core.permission import check_admin


async def logging(cmd, message, args):
    if not check_admin(message.author, message.channel):
        out_content = discord.Embed(type='rich', color=0xDB0000,
                                    title=':no_entry: Insufficient Permissions. Server Admin Only.')
        await cmd.bot.send_message(message.channel, None, embed=out_content)
        return
    try:
        loggin_active = cmd.db.get_settings(message.server.id, 'LoggingEnabled')
    except KeyError:
        cmd.db.set_settings(message.server.id, 'LoggingEnabled', False)
        loggin_active = False
    if loggin_active:
        cmd.db.set_settings(message.server.id, 'LoggingEnabled', False)
        out_content = discord.Embed(type='rich', color=0x66cc66,
                                    title=':white_check_mark: Logging Disabled.')
        await cmd.bot.send_message(message.channel, None, embed=out_content)
    else:
        cmd.db.set_settings(message.server.id, 'LoggingEnabled', True)
        out_content = discord.Embed(type='rich', color=0x66cc66,
                                    title=':white_check_mark: Logging Enabled.')
        await cmd.bot.send_message(message.channel, None, embed=out_content)
