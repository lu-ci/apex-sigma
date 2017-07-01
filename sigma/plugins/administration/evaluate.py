from config import permitted_id
import discord
import inspect


async def evaluate(cmd, message, args):
    if message.author.id in permitted_id:
        if not args:
            await message.channel.send(cmd.help())
        else:
            try:
                execution = " ".join(args)
                output = eval(execution)
                if inspect.isawaitable(output):
                    output = await output
                status = discord.Embed(title='✅ Executed', color=0x66CC66)
                if output:
                    try:
                        status.add_field(name='Results', value='\n```\n' + str(output) + '\n```')
                    except:
                        pass
            except Exception as e:
                cmd.log.error(e)
                status = discord.Embed(color=0xDB0000, title='❗ Error')
                status.add_field(name='Execution Failed', value=str(e))
            await message.channel.send(None, embed=status)
    else:
        status = discord.Embed(type='rich', color=0xDB0000,
                               title='⛔ Insufficient Permissions. Bot Owner or Server Admin Only.')
        await message.channel.send(None, embed=status)
