import discord

from config import permitted_id, Prefix


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
    return bool(author.id == bot_user.id)


def check_server_partner(db, server_id):
    try:
        partner = db.get_settings(server_id, 'IsPartner')
    except:
        db.set_settings(server_id, 'IsPartner', False)
        partner = False
    return partner


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


def check_man_srv(user, channel):
    return user.permissions_in(channel).manage_guild


def check_permitted(self, user, channel, server):
    if not self.perm['sfw'] and not check_channel_nsfw(self.db, channel.id):
        title = '🍆 Channel does not have NSFW permissions set, sorry.'
        explanation = 'To toggle NSFW permissions in a channel use the {:s} command.'.format(Prefix + 'nsfwpermit')
        explanation += '\nThis command is only usable by server administrators.'
        explanation += '\nIf you are the admin on your server, just type the command in the channel of your choice.'
        explanation += '\nOtherwise, ask your server\'s admin to permit a channel.'
        embed_content = discord.Embed(color=0x9933FF)
        embed_content.add_field(name=title, value=explanation)
        self.log.warning('NSFW: Access Denied.')
        return False, embed_content

    if self.perm['admin'] and not check_bot_owner(user):
        title = '⛔ Bot Owner Only'
        msg = 'Bot Owner commands are usable only by the owners of the bot as the name implies.'
        msg += '\nThe bot owner is the person hosting the bot on their machine.'
        msg += '\nThis is not the discord server owner and not the person who invited the bot to the server.'
        msg += '\nThere is no way for you to become a bot owner.'
        embed_content = discord.Embed(color=0xDB0000)
        embed_content.add_field(name=title, value=msg)
        self.log.warning('OWNER: Access Denied.')
        return False, embed_content

    if self.perm['partner'] and not check_server_partner(self.db, server.id):
        title = '💎 Partner Servers Only'
        msg = 'Some commands are limited to only be usable by partners.'
        msg += '\nYou can request to be a partner server by visiting our server and telling us why you should be one.'
        msg += '\nYou can also become a partner by supporting us via our '
        msg += '[`Patreon`](https://www.patreon.com/ApexSigma) page.'
        embed_content = discord.Embed(color=0x0099FF)
        embed_content.add_field(name=title, value=msg)
        self.log.warning('PARTNER: Access Denied.')
        return False, embed_content

    if not self.perm['pmable'] and not server and not is_self(user, self.bot.user):
        title = '⛔ This Function Is Not Usable in Direct Messages.'
        explanation = 'If you get this message, use the command on a server and not in a direct message.'
        embed_content = discord.Embed(color=0xDB0000)
        embed_content.add_field(name=title, value=explanation)
        self.log.warning('DM: Access Denied.')
        return False, embed_content

    return True, None
