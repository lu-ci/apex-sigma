import discord
from config import Prefix


async def pmdetect(ev, message, args):
    if not message.guild:
        ev.log.info(f'DM From {message.author.name}#{message.author.discriminator}: {message.content}')
        if not message.content.startswith(Prefix):
            pm_response = discord.Embed(color=0x0099FF, title=f'ℹ Type `{Prefix}help` for information!')
            await message.channel.send(None, embed=pm_response)
        else:
            cmd_name = message.content.split(' ')[0][len(Prefix):].lower()
            if cmd_name in ev.bot.alts:
                cmd_name = ev.bot.alts[cmd_name]
            if not cmd_name in ev.bot.plugin_manager.commands:
                pm_response = discord.Embed(color=0x696969, title='🔍 Not A Recognized Command')
                await message.channel.send(None, embed=pm_response)
