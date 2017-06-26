import yaml
import arrow
from config import permitted_id
import discord
import datetime
import sys


def stats(bot, log=None):
    tmp = []
    permed_ids = []
    for ownr in permitted_id:
        permed_ids.append(str(ownr))
    authors = userlist(bot.authors)
    donor_count = len(bot.donors)
    with open('VERSION') as version_file:
        content = yaml.safe_load(version_file)
        version = content['version']
        build_date = datetime.datetime.fromtimestamp(content['build_date']).strftime('%B %d, %Y')
        v_major = version['major']
        v_minor = version['minor']
        v_patch = version['patch']
        codename = content['codename']
        beta_state = content['beta']
    v_full = str(v_major) + '.' + str(v_minor) + '.' + str(v_patch)
    version_text = ''
    if beta_state:
        version_text += 'Beta '
    version_text += v_full + ' Codename ' + codename
    tmp.append(multi('Logged In As: \"' + bot.user.name + '\"', log))
    tmp.append(multi(f'Bot User ID: {bot.user.id}', log))
    tmp.append(multi('Python version: ' + sys.version.split(' ')[0], log))
    tmp.append(multi('discord.py version: ' + discord.__version__, log))
    tmp.append(multi('Authors: {:s}'.format(authors), log))
    tmp.append(multi('Donors: ' + str(donor_count), log))
    tmp.append(multi('Bot Version: ' + version_text, log))
    tmp.append(multi('Build Date: ' + build_date, log))
    tmp.append(multi('Connected to [ {:d} ] servers'.format(len(bot.guilds)), log))
    tmp.append(multi('Serving [ {:d} ] users'.format(len(list(bot.get_all_members()))), log))
    tmp.append(multi(f'Permitted IDs: {", ".join(permed_ids)}', log))
    return tmp


def userlist(lst):
    return ', '.join(['"{:s}"'.format(x) for x in lst])


def multi(msg, log=None):
    if log:
        log.info(msg)

    return msg


def add_cmd_stat(db, cmd, message):
    if not message.author.bot:
        command_data = {
            'name': cmd.name,
        }
        for key in ['global', 'sfw', 'admin', 'partner', 'pmable']:
            command_data[key] = cmd.perm[key]
        if message.guild:
            channel_id = message.channel.id
            guild_id = message.guild.id
        else:
            channel_id = None
            guild_id = None
        stat_data = {
            'command': command_data,
            'author': message.author.id,
            'channel': channel_id,
            'guild': guild_id,
            'timestamp': arrow.utcnow().timestamp
        }
        db.insert_one('CommandStats', stat_data)
