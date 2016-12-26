import discord
import time


async def donorize(cmd, message, args):
    if not args:
        await cmd.bot.send_message(message.channel, cmd.help())
    if len(args) < 2:
        await cmd.bot.send_message(message.channel, cmd.help())
    serv_id = args[0]
    don_time = args[1]
    current_time = int(time.time())
    expiration_stamp = current_time + int(don_time)
    donor_data = {
        'ServerID': serv_id,
        'Expiration': expiration_stamp
    }
    cmd.db.insert_one('DonorTracker', donor_data)
    status = discord.Embed(title=':white_check_mark: Added', color=0x66CC66)
    await cmd.bot.send_message(message.channel, None, embed=status)
