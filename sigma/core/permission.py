import discord
from time import time

from config import permitted_id


def check_channel_nsfw(db, channel_id):
    n = 0
    item = None
    finddata = {
        'ChannelID': channel_id,
    }
    finddata_res = db.find('NSFW', finddata)

    for item in finddata_res:
        n += 1

    if n == 0:
        return False
    else:
        active = item['Permitted']
        return active


def is_self(author, bot_user):
    if author.id == bot_user.id:
        return True
    else:
        return False


def check_server_donor(db, server_id):
    n = 0
    item = None
    finddata = {
        'ServerID': server_id
    }
    finddata_res = db.find('DonorTracker', finddata)

    for item in finddata_res:
        n += 1

    if n == 0:
        is_donor = False
    else:
        expiration_ts = item['Expiration']
        current_ts = int(time())
        is_donor = expiration_ts > current_ts

    return is_donor


def set_channel_nsfw(db, channel_id):
    n = 0
    item = None
    coll = 'NSFW'
    finddata = {
        'ChannelID': channel_id,
    }
    finddata_res = db.find(coll, finddata)

    for item in finddata_res:
        n += 1

    if n == 0:
        insertdata = {
            'ChannelID': channel_id,
            'Permitted': True
        }
        db.insert_one(coll, insertdata)
        success = True
    else:
        permitted = item['Permitted']
        updatetarget = {"ChannelID": channel_id}
        updatepermit = {"$set": {"Permitted": not permitted}}
        db.update_one(coll, updatetarget, updatepermit)
        success = not permitted

    return success


def check_bot_owner(user):
    return user.id in permitted_id


def check_admin(user, channel):
    return user.permissions_in(channel).administrator


def check_ban(user, channel):
    return user.permissions_in(channel).ban_members


def check_kick(user, channel):
    return user.permissions_in(channel).kick_members


def check_man_msg(user, channel):
    return user.permissions_in(channel).manage_messages


def check_man_roles(user, channel):
    return user.permissions_in(channel).manage_roles


def check_write(user, channel):
    return user.permissions_in(channel).send_messages


def check_man_chan(user, channel):
    return user.permissions_in(channel).manage_channels


def check_permitted(self, user, channel, server):
    if not self.perm['sfw'] and not check_channel_nsfw(self.db, channel.id):
        title = ':eggplant: Channel does not have NSFW permissions set, sorry.'
        explanation = 'To toggle NSFW permissions in a channel use the {:s} command.'
        explanation += '\nThis command is only usable by server administrators.'
        explanation += '\nIf you are the admin on your server, just type the command in the channel of your choice.'
        explanation += '\nOtherwise, ask your server\'s admin to permit a channel.'
        embed_content = discord.Embed(color=0x9933FF)
        embed_content.add_field(name=title, value=explanation)
        self.log.info('Access Denied Due To Channel Not Having NSFW Permissions.')
        return False, embed_content

    if self.perm['admin'] and not check_bot_owner(user):
        title = ':no_entry: Unpermitted'
        msg = 'Bot Owne r commands are usable only by the owners of the bot as the name implies.'
        msg += '\nThe bot owner is the person hosting the bot on their machine.'
        msg += '\nThis is **not the discord server owner** and **not the person who invited the bot** to the server.'
        msg += '\nThere is no way for you to become a bot owner.'
        embed_content = discord.Embed(title=title, color=0xDB0000)
        embed_content.add_field(name='Bot Owner Only', value=msg)
        self.log.info('Access Denied To A Bot Owner Only Command.')
        return False, embed_content

    if self.perm['donor'] and not check_server_donor(self.db, server.id):
        title = ':warning: Unpermitted'
        msg = 'Some commands are limited to only be usable by donors.'
        msg += '\nYou can become a donor by donating via our [`Paypal.Me`](https://www.paypal.me/AleksaRadovic) page.'
        msg += '\nDonating allows use of donor functions for a limited time.'
        msg += '\n1 Cent = One Hour (Currency of Calculation is Euro)'
        msg += '\nIn a nutshell, donating 7.2Eur would give you a month of donor functions.'
        embed_content = discord.Embed(title=title, color=0xFF9900)
        embed_content.add_field(name='Donor Only', value=msg)
        self.log.info('Access Denied To A Donor Only Command.')
        return False, embed_content

    if not self.perm['pmable'] and not server and not is_self(user, self.bot.user):
        title = ':no_entry: This Function Is Not Usable in Direct Messages.'
        explanation = 'Most commands are server bound or have no sense in being used in private messages'
        embed_content = discord.Embed(color=0xDB0000)
        embed_content.add_field(name=title, value=explanation)
        self.log.info('Access Denied To A DM Incompatible Command.')
        return False, embed_content

    return True, None
