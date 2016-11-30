import time
import asyncio

from sigma.core.formatting import bold


async def remind(cmd, message, args):
    remind_text = 'Nothing'
    time_q = 0
    if args:
        if len(args) < 2:
            await cmd.bot.send_message(message.channel, cmd.help())
            return
        else:
            if args and args[0] and args[1]:
                time_q = int(args[0])
                remind_text = ' '.join(args[1:])
            else:
                msg = 'Input missing parameters.\n\n{:s}'.format(cmd.help())
                await cmd.bot.send_message(message.channel, msg)
                return

            try:
                time_conv = time.strftime('%H:%M:%S', time.gmtime(time_q))

                msg = 'Okay! Reminder for\n[{:s}]\nis set and will be activated in `{:s}`! :clock:'.format(
                    bold(remind_text), time_conv)
                await cmd.bot.send_message(message.channel, msg)
                await asyncio.sleep(time_q)
                msg = '<@{:s}> Time\'s up! Let\'s do this! :clock: \n :exclamation: {:s} :exclamation: '.format(
                    message.author.id, remind_text)
                await cmd.bot.send_message(message.channel, msg)
            except Exception as e:
                cmd.log.error(e)
                await cmd.bot.send_message(message.channel, 'Something went wrong with setting the timer, are you sure you inputed a number?')
    else:
        await cmd.bot.send_message(message.channel, cmd.help())
        return
