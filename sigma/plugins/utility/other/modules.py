import discord

async def modules(cmd, message, args):
    embed_to_user = discord.Embed(color=0x1abc9c)
    embed_to_user.add_field(name='🔍 Sigma\'s Module Group List', value='```yaml\n' + '\n'.join(cmd.bot.module_list) + '\n```')
    await message.author.send(None, embed=embed_to_user)
    if message.guild:
        embed_local = discord.Embed(color=0x66CC66, title='✅ List Sent To Your DM')
        await message.channel.send(None, embed=embed_local)
