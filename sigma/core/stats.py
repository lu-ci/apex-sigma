import yaml
from config import permitted_id
import discord
import datetime
import sys


def stats(bot, log=None):
    tmp = []
    permed_ids = userlist(permitted_id)
    authors = userlist(bot.authors)
    contributors = userlist(bot.contributors)
    donor_count = len(bot.donors)
    with open('VERSION') as version_file:
        content = yaml.load(version_file)
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
    tmp.append(multi('Bot User ID: ' + bot.user.id, log))
    tmp.append(multi('Python version: ' + sys.version.split(' ')[0], log))
    tmp.append(multi('discord.py version: ' + discord.__version__, log))
    tmp.append(multi('Authors: {:s}'.format(authors), log))
    tmp.append(multi('Contributors: {:s}'.format(contributors), log))
    tmp.append(multi('Donors: ' + str(donor_count), log))
    tmp.append(multi('Bot Version: ' + version_text, log))
    tmp.append(multi('Build Date: ' + build_date, log))
    tmp.append(multi('Connected to [ {:d} ] servers'.format(len(bot.servers)), log))
    tmp.append(multi('Serving [ {:d} ] users'.format(len(list(bot.get_all_members()))), log))
    tmp.append(multi('Permitted IDs: {:s}'.format(permed_ids), log))
    return tmp


def userlist(lst):
    return ', '.join(['"{:s}"'.format(x) for x in lst])


def multi(msg, log=None):
    if log:
        log.info(msg)

    return msg
