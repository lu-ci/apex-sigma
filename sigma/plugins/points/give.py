import discord


async def give(cmd, message, args):
    if not args:
        await cmd.bot.send_message(message.channel, cmd.help())
        return
    if not message.mentions:
        await cmd.bot.send_message(message.channel, cmd.help())
        return
    if len(args) < 2:
        await cmd.bot.send_message(message.channel, cmd.help())
        return
    target_user = message.mentions[0]
    if target_user.bot:
        return
    if target_user == message.author:
        return
    amount = abs(int(args[0]))
    curr_points = cmd.db.get_points(message.server, message.author)
    if amount > curr_points:
        out_content = discord.Embed(type='rich', color=0xDB0000,
                                    title='⛔ You Do Not Have Enough Points.')
        await cmd.bot.send_message(message.channel, None, embed=out_content)
        return
    else:
        cmd.db.take_points(message.server, message.author, amount)
        cmd.db.add_points(message.server, target_user, amount)
        out_content = discord.Embed(type='rich', color=0x66CC66,
                                    title='✅ Points Transferred.')
        await cmd.bot.send_message(message.channel, None, embed=out_content)
