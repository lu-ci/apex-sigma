from config import permitted_id
import asyncio

async def evaluate(cmd, message, args):
    if message.author.id in permitted_id:
        if not args:
            await cmd.reply(cmd.help())
        else:
            try:
                execution = ' '.join(args)
                output = eval(execution)
                out_text = 'Executed.'
                try:
                    out_text += '\n```\n' + str(output) + '\n```'
                except:
                    pass
                await cmd.reply(out_text)
            except Exception as e:
                cmd.log.error(e)
                await cmd.reply('Execution failed.\n' + str(e))
    else:
        response = await cmd.reply('Unpermitted. :x:')
        await asyncio.sleep(10)
        await cmd.bot.delete_message(response)
