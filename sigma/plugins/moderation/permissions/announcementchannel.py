from sigma.core.permission import check_admin
from sigma.core.permission import check_write
from config import Prefix
import discord


async def announcementchannel(cmd, message, args):
    if not check_admin(message.author, message.channel):
        # user is no server admin
        embed = discord.Embed(title='⛔ Unpermitted. Server Admin Only.', color=0xDB0000)
    else:
        if message.channel_mentions:
            # argument exists and is a channel
            newchannel = message.channel_mentions[0]
            writable = check_write(message.guild.get_member(cmd.bot.user.id), newchannel)
            if writable:
                # channel can be written to -> turn on announcements and set channelid
                cmd.db.set_settings(message.guild.id, 'Announcement', True)
                cmd.db.set_settings(message.guild.id, 'AnnouncementChannel', newchannel.id)
                embed = discord.Embed(
                    title='✅ Announcements will be posted to #' + newchannel.name, color=0x66CC66)
            else:
                embed = discord.Embed(title='⛔ Missing write permissions for this channel', color=0xDB0000)
        else:
            if len(args) == 0:
                # no argument given, announcements will be turned off
                cmd.db.set_settings(message.guild.id, 'Announcement', False)
                embed = discord.Embed(title='✅ Announcements turned OFF for this server',
                                      color=0x66CC66)
                embed.add_field(name='Note:',
                                value='Use "' + Prefix + 'announcementchannel #channel_name" to turn them back on.')
            else:
                # given argument is not a channel
                embed = discord.Embed(title=':x: "' + args[0] + '" is not a channel', color=0xDB0000)
                embed.add_field(name='Note:',
                                value='Enter a channel in this format: "#channel_name" or leave blank to turn announcements off.')
    await message.channel.send(None, embed=embed)
