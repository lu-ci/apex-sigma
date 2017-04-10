import discord
from config import permitted_id


async def kill(cmd, message, args):
    if message.author.id in permitted_id:
        status = discord.Embed(title=':skull_crossbones: Sigma Shutting Down.', color=0x808080)
        try:
            await message.channel.send(None, embed=status)
        except:
            pass
        cmd.log.info('Terminated by user {:s}'.format(message.author.name))
        await cmd.bot.logout()
        await cmd.bot.close()
