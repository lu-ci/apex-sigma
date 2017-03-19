from sigma.core.permission import check_admin
import discord

async def markovtoggle(cmd, message, args):
    if check_admin(message.author, message.channel):
        active = cmd.db.get_settings(message.server.id, 'MarkovCollect')
        if active:
            cmd.db.set_settings(message.server.id, 'MarkovCollect', False)
            out_content = discord.Embed(type='rich', color=0x66CC66,
                                        title='✅ Markov Collection Disabled')
        else:
            cmd.db.set_settings(message.server.id, 'MarkovCollect', True)
            out_content = discord.Embed(type='rich', color=0x66CC66,
                                        title='✅ Markov Collection Enabled')
    else:
        out_content = discord.Embed(type='rich', color=0xDB0000,
                                    title=':no_entry: Insufficient Permissions. Server Admin Only.')
    await cmd.bot.send_message(message.channel, None, embed=out_content)
