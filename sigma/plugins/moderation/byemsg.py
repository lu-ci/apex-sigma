import discord
from sigma.core.permission import check_admin


async def byemsg(cmd, message, args):
    if not args:
        bye_message = cmd.db.get_settings(message.guild.id, 'ByeMessage')
        embed = discord.Embed(color=0x0099FF)
        embed.add_field(name='ℹ Current Bye Message', value='```\n' + bye_message + '\n```')
    else:
        if not check_admin(message.author, message.channel):
            embed = discord.Embed(title='⛔ Unpermitted', color=0xDB0000)
        else:
            new_message = ' '.join(args)
            cmd.db.set_settings(message.guild.id, 'ByeMessage', new_message)
            embed = discord.Embed(title='✅ New Bye Message Set', color=0x66CC66)
    await message.channel.send(None, embed=embed)
