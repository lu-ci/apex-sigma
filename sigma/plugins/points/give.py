import discord
from config import Currency

async def give(cmd, message, args):
    if not args:
        await message.channel.send(cmd.help())
        return
    if not message.mentions:
        await message.channel.send(cmd.help())
        return
    if len(args) < 2:
        await message.channel.send(cmd.help())
        return
    target_user = message.mentions[0]
    if target_user.bot:
        return
    if target_user == message.author:
        return
    amount = abs(int(args[0]))
    curr_points = cmd.db.get_points(message.author)['Current']
    if amount > curr_points:
        out_content = discord.Embed(color=0xDB0000, title=f'⛔ You Do Not Have Enough {Currency}.')
        await message.channel.send(None, embed=out_content)
        return
    else:
        cmd.db.take_points(message.server, message.author, amount)
        cmd.db.add_points(message.server, target_user, amount)
        out_content = discord.Embed(color=0x66CC66, title=f'✅ {Currency} Transferred.')
        await message.channel.send(None, embed=out_content)
