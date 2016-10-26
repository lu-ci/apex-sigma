import yaml
from config import permitted_id
import discord


def stats(bot, log=None):
    permed_ids = userlist(permitted_id)
    authors = userlist(bot.authors)
    contributors = userlist(bot.contributors)
    donors = userlist(bot.donors)
    with open('VERSION') as version_file:
        content = yaml.load(version_file)
        version = content['version']
        codename = content['codename']
        beta_state = content['beta']
    version_text = ''
    if beta_state:
        version_text += 'Beta '
    version_text += 'v' + str(version) + ' Codename ' + codename


    tmp = []
    tmp.append(multi('Logged In As: \"' + bot.user.name + '\"', log))
    tmp.append(multi('Bot User ID: ' + bot.user.id, log))
    tmp.append(multi('Running discord.py version: ' + discord.__version__, log))
    tmp.append(multi('Authors: {:s}'.format(authors), log))
    tmp.append(multi('Contributors: {:s}'.format(contributors), log))
    tmp.append(multi('Donors: {:s}'.format(donors), log))
    tmp.append(multi('Bot Version: ' + version_text, log))
    tmp.append(multi('Build Date: 16. October 2016.', log))
    tmp.append(multi('Connected to [ {:d} ] servers'.format(bot.server_count), log))
    tmp.append(multi('Serving [ {:d} ] users'.format(bot.member_count), log))
    tmp.append(multi('Permitted IDs: {:s}'.format(permed_ids), log))

    return tmp


def userlist(lst):
    return ', '.join(['"{:s}"'.format(x) for x in lst])

def multi(msg, log=None):
    if log:
        log.info(msg)

    return msg
