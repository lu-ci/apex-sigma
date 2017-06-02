import discord
from sigma.core.permission import check_admin


async def loggingchannel(cmd, message, args):
    if not check_admin(message.author, message.channel):
        response = discord.Embed(title='⛔ Unpermitted. Server Admin Only.', color=0xDB0000)
    else:
        if message.channel_mentions:
            target_chn = message.channel_mentions[0]
        else:
            if args:
                if args[0].lower() == 'disable':
                    cmd.db.set_settings(message.guild.id, 'LoggingChannel', None)
                    response = discord.Embed(color=0x66CC66, title=f'✅ Logging channel disabled.')
                    await message.channel.send(embed=response)
                    return
                else:
                    target_chn = message.channel
            else:
                target_chn = None
        if target_chn:
            cmd.db.set_settings(message.guild.id, 'LoggingChannel', target_chn.id)
            response = discord.Embed(color=0x66CC66, title=f'✅ #{target_chn.name} set as the logging channel.')
        else:
            response = discord.Embed(color=0xDB0000, title='❗ No channel tagged.')
    await message.channel.send(embed=response)
