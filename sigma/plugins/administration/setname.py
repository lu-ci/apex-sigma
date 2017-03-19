import discord
from config import permitted_id


async def setname(cmd, message, args):
    if message.author.id in permitted_id:
        if not args:
            await cmd.bot.send_message(message.channel, cmd.help())
            return
        else:
            username = ' '.join(args)
            await cmd.bot.edit_profile(username=username)
            embed = discord.Embed(title='✅ Changed Username', color=0x66CC66)
            await cmd.bot.send_message(message.channel, None, embed=embed)
    else:
        out = discord.Embed(type='rich', color=0xDB0000,
                            title=':no_entry: Insufficient Permissions. Bot Owner Only.')
        await cmd.bot.send_message(message.channel, None, embed=out)
