from config import permitted_id
from sigma.core.permission import check_admin
from sigma.core.permission import check_write
from config import Prefix
import discord

async def announcementchannel(cmd, message, args):
	#TODO: channels.permissions_for() <- check if channel can be written to
	embed=discord.Embed(title='nix is passiert :no_mouth:', color=0xDB0000)
	if not check_admin(message.author, message.channel):
		#user is no server admin
		embed = discord.Embed(title=':no_entry: Unpermitted. Server Admin Only.', color=0xDB0000)
	else:
		if len(args)>0 and cmd.bot.get_channel(args[0][2:-1]) != None:
			#argument exists and is a channel
			newChannel=cmd.bot.get_channel(args[0][2:-1])
			if message.server.id == newChannel.server.id:
				#channel is from this server 
				if check_write(message.server.get_member(cmd.bot.user.id),newChannel):
					#channel can be written to -> turn on announcements and set channelid
					await cmd.bot.send_message(message.channel, 'yepp, du darfst')
					cmd.db.set_settings(message.server.id, 'Announcement', True)
					cmd.db.set_settings(message.server.id, 'AnnouncementChannel', newChannel.id)
					embed = discord.Embed(title=':white_check_mark: Announcements will be posted to #'+newChannel.name, color=0x66CC66)
				else:
					embed = discord.Embed(title=':no_entry: Missing write permissions for this channel', color=0xDB0000)
			else:
				#channel is not from this server
				embed = discord.Embed(title=':no_entry: Unpermitted. This channel isn\'t from this server', color=0xDB0000)
		else:
			if len(args)==0:
				#no argument given, announcements will be turned off
				cmd.db.set_settings(message.server.id, 'Announcement', False)
				embed = discord.Embed(title=':white_check_mark: Announcements turned OFF for this server', color=0x66CC66)
				embed.add_field(name='Note:', value='Use "'+Prefix+'announcementchannel #channel_name" to turn them back on.')
			else:
				#given argument is not a channel
				embed = discord.Embed(title=':x: "'+args[0]+'" is not a channel', color=0xDB0000)
				embed.add_field(name='Note:', value='Enter a channel in this format: "#channel_name" or leave blank to turn announcements off.')
	await cmd.bot.send_message(message.channel, None, embed=embed)