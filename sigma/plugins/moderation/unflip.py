from sigma.core.permission import check_admin
import discord

async def unflip(cmd, message, args):
    if check_admin(message.author, message.channel):
        active = cmd.db.get_settings(message.guild.id, 'Unflip')
        if active:
            cmd.db.set_settings(message.guild.id, 'Unflip', False)
            out_content = discord.Embed(type='rich', color=0x66CC66,
                                        title='✅ Automatic Table Un-Flipping Disabled')
        else:
            cmd.db.set_settings(message.guild.id, 'Unflip', True)
            out_content = discord.Embed(type='rich', color=0x66CC66,
                                        title='✅ Automatic Table Un-Flipping Enabled')
    else:
        out_content = discord.Embed(type='rich', color=0xDB0000,
                                    title='⛔ Insufficient Permissions. Server Admin Only.')
    await message.channel.send(None, embed=out_content)
