import discord
from config import permitted_id


async def kill(cmd, message, args):
    if message.author.id in permitted_id:
        status = discord.Embed(title=':skull_crossbones: Sigma Shutting Down.', color=0x808080)
        await cmd.bot.send_message(message.channel, None, embed=status)
        await cmd.bot.logout()
        cmd.log.info('Terminated by user {:s}'.format(message.author.name))
        exit('Terminated by command.')
