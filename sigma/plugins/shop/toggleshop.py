import discord
from sigma.core.permission import check_admin


async def toggleshop(cmd, message, args):
    if not check_admin(message.author, message.channel):
        status = discord.Embed(type='rich', color=0xDB0000,
                               title=':no_entry: Insufficient Permissions. Server Admin Only.')
    else:
        shop_enabled = cmd.db.get_settings(message.server.id, 'ShopEnabled')
        if shop_enabled:
            cmd.db.set_settings(message.server.id, 'ShopEnabled', False)
            status = discord.Embed(type='rich', color=0x66CC66,
                                   title='✅ The shop has been Disabled.')
        else:
            cmd.db.set_settings(message.server.id, 'ShopEnabled', True)
            status = discord.Embed(type='rich', color=0x66CC66,
                                   title='✅ The shop has been Enabled.')
    await cmd.bot.send_message(message.channel, None, embed=status)
