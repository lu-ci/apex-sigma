import time
import datetime
import asyncio
import discord


async def remind(cmd, message, args):
    remind_text = 'No Reminder Text'
    current_time = time.time()
    if args:
        try:
            time_q = int(args[0])
        except:
            embed = discord.Embed(title=':exclamation: Not A Number', color=0xDB0000)
            await cmd.bot.send_message(message.channel, None, embed=embed)
            return
        if len(args) > 1:
            remind_text = ' '.join(args[1:])
        timestamp = (time_q + current_time) * 1000
        date = datetime.datetime.fromtimestamp(timestamp / 1e3)
        embed = discord.Embed(title=':clock: Reminder Set.', timestamp=date,
                              color=0x1abc9c)
        embed.add_field(name='Reminder Message', value='```\n' + remind_text + '\n```')
        embed.add_field(name='Time Until Reminder',
                        value='```\n' + time.strftime('%H:%M:%S', time.gmtime(time_q)) + '\n```')
        await cmd.bot.send_message(message.channel, None, embed=embed)
        await asyncio.sleep(time_q)
        embed = discord.Embed(color=0x1abc9c)
        embed.add_field(name=':clock: Time\'s Up!', value=remind_text)
        await cmd.bot.send_message(message.channel, 'Hey <@' + message.author.id + '>!', embed=embed)
    else:
        await cmd.bot.send_message(message.channel, cmd.help())
        return
