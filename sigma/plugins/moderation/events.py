import discord
from sigma.core.permission import check_admin


async def events(cmd, message, args):
    if not check_admin(message.author, message.channel):
        out_content = discord.Embed(type='rich', color=0xDB0000,
                                    title=':no_entry: Insufficient Permissions. Server Admin Only.')
        await cmd.bot.send_message(message.channel, None, embed=out_content)
        return
    events_enabled = cmd.db.get_settings(message.server.id, 'RandomEvents')
    if events_enabled:
        cmd.db.set_settings(message.server.id, 'RandomEvents', False)
        out_content = discord.Embed(type='rich', color=0x66cc66,
                                    title=':white_check_mark: Random Events have been Disabled.')
        await cmd.bot.send_message(message.channel, None, embed=out_content)
    else:
        cmd.db.set_settings(message.server.id, 'RandomEvents', True)
        out_content = discord.Embed(type='rich', color=0x66cc66,
                                    title=':white_check_mark: Random Events have been Enabled.')
        await cmd.bot.send_message(message.channel, None, embed=out_content)
