import discord


async def blockedwords(cmd, message, args):
    try:
        blacklist = cmd.db.get_settings(message.guild.id, 'BlockedWords')
    except:
        cmd.db.set_settings(message.guild.id, 'BlockedWords', [])
        blacklist = []
    if blacklist:
        response = discord.Embed(color=0x0099FF)
        response.add_field(name='ℹ List of Blocked Words', value=f'```\n{", ".join(blacklist)}\n```')
    else:
        response = discord.Embed(color=0x0099FF, title='ℹ No Blocked Words Found')
    await message.channel.send(embed=response)
