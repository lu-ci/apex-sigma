import time
import asyncio

from sigma.core.formatting import bold


async def remind(cmd, message, args):
    remind_text = 'Nothing'
    time_q = 0
    if args:
        if len(args) < 2:
            await cmd.reply(cmd.help())
            return
        else:
            if args and args[0] and args[1]:
                time_q = int(args[0])
                remind_text = ' '.join(args[1:])
            else:
                msg = 'Input missing parameters.\n\n{:s}'.format(cmd.help())
                await cmd.reply(msg)
                return

            try:
                time_conv = time.strftime('%H:%M:%S', time.gmtime(time_q))

                msg = 'Okay! Reminder for\n[{:s}]\nis set and will be activated in `{:s}`! :clock:'.format(
                    bold(remind_text), time_conv)
                await cmd.reply(msg)
                await asyncio.sleep(time_q)
                msg = '<@{:s}> Time\'s up! Let\'s do this! :clock: \n :exclamation: {:s} :exclamation: '.format(
                    message.author.id, remind_text)
                await cmd.reply(msg)
            except Exception as e:
                cmd.log.error(e)
                await cmd.reply('Something went wrong with setting the timer, are you sure you inputed a number?')
    else:
        await cmd.reply(cmd.help())
        return
