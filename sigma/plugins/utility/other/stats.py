import sys
import arrow
import discord
import datetime
from config import permitted_id

async def stats(cmd, message, args):
    sigma_avatar = 'https://i.imgur.com/mGyqMe1.png'
    current_time = arrow.utcnow().timestamp
    upseconds = current_time - cmd.bot.start_time
    permed_ids = []
    for ownr in permitted_id:
        permed_ids.append(str(ownr))
    uptime = str(datetime.timedelta(seconds=upseconds))
    owners = ', '.join(permed_ids)
    if message.guild:
        for m in message.guild.members:
            if m.id in permitted_id:
                if m.nick:
                    owners = owners.replace(str(m.id), m.nick)
                else:
                    owners = owners.replace(str(m.id), m.name)
    full_version = f'{cmd.bot.v_major}.{cmd.bot.v_minor}.{cmd.bot.v_patch}'
    command_rate = str(cmd.bot.command_count / upseconds)
    command_rate = command_rate.split('.')
    command_rate = command_rate[0] + '.' + command_rate[1][:3]
    message_rate = str(cmd.bot.message_count / upseconds)
    message_rate = message_rate.split('.')
    message_rate = message_rate[0] + '.' + message_rate[1][:3]
    embed = discord.Embed(color=0x1abc9c)
    embed.set_author(name='Apex Sigma', url='https://auroraproject.xyz/', icon_url=sigma_avatar)
    embed.add_field(name='Logged In As', value=f'```py\n{cmd.bot.user.name} [{cmd.bot.user.id}]\n```', inline=False)
    embed.add_field(name='Authors', value=f'```\n{", ".join(cmd.bot.authors)}\n```', inline=False)
    embed.add_field(name='Bot Version', value=f'```py\n{full_version}\n```')
    embed.add_field(name='Bot Codename', value=f'```py\n"{cmd.bot.codename}"\n```')
    if args:
        if args[0].lower() == 'full':
            embed.add_field(name='Build Date', value=f'```py\n{cmd.bot.build_date.format("DD-MM-YYYY")}\n```')
            embed.add_field(name='Environment', value=f'```py\nPython {sys.version.split(" ")[0]}\n```', inline=True)
            embed.add_field(name='API Wrapper', value=f'```py\nd.py {discord.__version__}\n```', inline=True)
            embed.add_field(name='Uptime', value=f'```py\n{uptime}\n```', inline=True)
            embed.add_field(name='Servers', value=f'```py\n{len(cmd.bot.guilds)}\n```')
            embed.add_field(name='Channels', value=f'```py\n{len(list(cmd.bot.get_all_channels()))}\n```')
            embed.add_field(name='Users', value=f'```py\n{len(list(cmd.bot.get_all_members()))}\n```')
            embed.add_field(name='Commands Executed', value=f'```py\n{cmd.bot.command_count} ({command_rate}/s)\n```', inline=True)
            embed.add_field(name='Messages Processed', value=f'```py\n{cmd.bot.message_count} ({message_rate}/s)\n```', inline=True)
    embed.add_field(name='Bot Owners', value=f'```\n{owners}\n```', inline=False)
    await message.channel.send(None, embed=embed)
