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
        await cmd.bot.send_message(message.channel, 'You can not give points to bots.')
        return
    amount = abs(int(args[0]))
    curr_points = cmd.db.get_points(message.server, message.author)
    if amount > curr_points:
        await cmd.bot.send_message(message.channel,
                                   'You don\'t seem have enough points, <@' + message.author.id + '>...\nYou wanted to transfer **' + str(
                                       amount) + '** while you only have **' + str(curr_points) + '**.')
        return
    else:
        cmd.db.take_points(message.server, message.author, amount)
        cmd.db.add_points(message.server, target_user, amount)
        await cmd.bot.send_message(message.channel, 'Alright <@' + message.author.id + '>, I\'ve transfered **' + str(
            amount) + '** points to <@' + target_user.id + '>!')
