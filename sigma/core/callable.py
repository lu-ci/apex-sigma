import discord
import os
from importlib import import_module
from config import permitted_id

from .permission import check_channel_nsfw, check_server_donor, is_self


class NotEnabledError(RuntimeError):
    pass


class Callable(object):
    def __init__(self, plugin, info):
        self.enabled = False
        self.glob = False
        self.sfw = True
        self.admin = False
        self.donor = False
        self.pmable = False
        self.usage = 'No usage info available.'
        self.desc = 'No description available.'

        self.db = plugin.db
        self.log = plugin.log
        self.bot = plugin.bot
        self.plugin = plugin

        try:
            self.load_info(info)
        except NotEnabledError:
            return

    def load_info(self, info):
        if 'enabled' not in info or not info['enabled']:
            raise NotEnabledError
        else:
            self.enabled = True

        self.name = info['name']
        self.path = self.plugin.path

        if 'global' in info and info['global']:
            self.glob = True

        if 'usage' in info:
            self.usage = info['usage']

        if 'description' in info:
            self.desc = info['description']

        self.sfw = info['sfw']
        if 'admin' in info:
            self.admin = info['admin']
        if 'donor' in info:
            self.donor = info['donor']
        if 'pmable' in info:
            self.pmable = info['pmable']

        module_path = os.path.join(self.path, self.name)
        self.modpath = module_path.replace('/', '.').replace('\\', '.')
        self.module = import_module(self.modpath)

    def resource(self, path):
        return os.path.join(self.path, 'res', path)

    def help(self):
        return ''

    async def call(self, message, *args):
        channel = message.channel
        msg = None
        black_channel = False
        black_user = False
        server_is_black = False
        if message.author.bot:
            return
        if message.server:
            channel_blacklist = self.db.get_settings(message.server.id, 'BlacklistedChannels')
            if not channel_blacklist:
                channel_blacklist = []
            user_blacklist = self.db.get_settings(message.server.id, 'BlacklistedUsers')
            if not user_blacklist:
                user_blacklist = []
            if message.author.id in user_blacklist:
                black_user = True
            if message.channel.id in channel_blacklist:
                black_channel = True
            server_is_black = self.db.get_settings(message.server.id, 'IsBlacklisted')
        if message.author.id not in permitted_id:
            if black_channel or black_user or server_is_black:
                return
        if not self.sfw and not check_channel_nsfw(self.db, channel.id):
            embed_content = discord.Embed(title=':eggplant: Channel does not have NSFW permissions set, sorry.',
                                          color=0x9933FF)
            await self.bot.send_message(channel, None, embed=embed_content)
            return
        if self.admin and message.author.id not in permitted_id:
            bot_owner_text = 'Bot Owner commands are usable only by the owners of the bot as the name implies.'
            bot_owner_text += '\nThe bot owner is the person hosting the bot on their machine.'
            bot_owner_text += '\nThis is **not the discord server owner**, and it is **not the person who invited the bot** to the server.'
            bot_owner_text += '\nThere is no way for you to become a bot owner.'
            embed_content = discord.Embed(title=':no_entry: Unpermitted', color=0xDB0000)
            embed_content.add_field(name='Bot Owner Only', value=bot_owner_text)
            await self.bot.send_message(channel, None, embed=embed_content)
            return
        if self.donor and not check_server_donor(self.db, message.server.id):
            donor_deny_info = 'Some commands are limited to only be usable by donors.'
            donor_deny_info += '\nYou can become a donor by donating via our [`Paypal.Me`](https://www.paypal.me/AleksaRadovic) page.'
            donor_deny_info += '\nDonating allows use of donor functions for a limited time.'
            donor_deny_info += '\n1 Cent = One Hour (Currency of Calculation is Euro)'
            donor_deny_info += '\nIn a nutshell, donating 7.2Eur would give you a month of donor functions.'
            embed_content = discord.Embed(title=':warning: Unpermitted', color=0xFF9900)
            embed_content.add_field(name='Donor Only', value=donor_deny_info)
            await self.bot.send_message(channel, None, embed=embed_content)
            return
        if not self.pmable and not message.server and not is_self(self, message.author, self.bot.user):
            embed_content = discord.Embed(title=':no_entry: This Function Is Not Usable in Direct Messages.',
                                          color=0xDB0000)
            await self.bot.send_message(channel, None, embed=embed_content)
            return
        try:
            msg = await getattr(self.module, self.name)(self, message, *args)
        except Exception as e:
            try:
                self.log.error(str(e))
                error_embed = discord.Embed(color=0xDB0000)
                error_embed.add_field(name=':exclamation: An Error Occurred!', value='```\n' + str(e) + '\n```')
                error_embed.set_footer(
                    text='For more information you can go to the AP Discord server and ask us, the link is in the help.')
                await self.bot.send_message(channel, None, embed=error_embed)
            except:
                pass

        if not self.sfw and check_channel_nsfw(self.db, channel.id):
            self.db.add_stats('NSFWCount')

        if msg:
            await self.bot.send_message(channel, msg)

    async def call_sp(self, member):
        msg = await getattr(self.module, self.name)(self, member)
