import sys
import arrow
import discord
import datetime
from config import permitted_id

async def stats(cmd, message, args):
    sigma_avatar = 'https://i.imgur.com/mGyqMe1.png'
    current_time = arrow.utcnow().timestamp
    upseconds = current_time - cmd.bot.start_time
    uptime = str(datetime.timedelta(seconds=upseconds))
    owners = ', '.join(permitted_id)
    if message.server:
        for m in message.server.members:
            if m.id in permitted_id:
                if m.nick:
                    owners = owners.replace(m.id, m.nick)
                else:
                    owners = owners.replace(m.id, m.name)
    full_version = f'{cmd.bot.v_major}.{cmd.bot.v_minor}.{cmd.bot.v_patch}'
    embed = discord.Embed(color=0x1abc9c)
    embed.set_author(name='Apex Sigma', url='https://auroraproject.xyz/', icon_url=sigma_avatar)
    embed.add_field(name='Logged In As', value=f'```py\n{cmd.bot.user.name} [{cmd.bot.user.id}]\n```', inline=False)
    embed.add_field(name='Authors', value=f'```\n{", ".join(cmd.bot.authors)}\n```', inline=False)
    embed.add_field(name='Environment', value=f'```py\nPython {sys.version.split(" ")[0]}\n```', inline=True)
    embed.add_field(name='API Wrapper', value=f'```py\ndiscord.py {discord.__version__}\n```', inline=True)
    embed.add_field(name='Uptime', value=f'```py\n{uptime}\n```', inline=True)
    embed.add_field(name='Bot Version', value=f'```py\n{full_version}\n```')
    embed.add_field(name='Bot Codename', value=f'```py\n"{cmd.bot.codename}"\n```')
    embed.add_field(name='Build Date', value=f'```py\n{cmd.bot.build_date.format("DD-MM-YYYY")}\n```')
    embed.add_field(name='Servers', value=f'```py\n{len(cmd.bot.servers)}\n```')
    embed.add_field(name='Channels', value=f'```py\n{len(list(cmd.bot.get_all_channels()))}\n```')
    embed.add_field(name='Users', value=f'```py\n{len(list(cmd.bot.get_all_members()))}\n```')
    embed.add_field(name='Bot Owners', value=f'```\n{owners}\n```', inline=False)
    await message.channel.send(None, embed=embed)
