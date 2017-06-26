import discord
import os
from importlib import import_module
from config import DevMode
from .formatting import codeblock
from .resource import global_resource
from .permission import check_permitted

if DevMode:
    exception = SyntaxError
else:
    exception = Exception


class NotEnabledError(RuntimeError):
    pass


class Callable(object):
    def __init__(self, plugin, info):
        self.enabled = False
        self.usage = 'No usage info available.'
        self.desc = 'No description available.'
        self.perm = {
            'global': False,
            'sfw': True,
            'admin': False,
            'partner': False,
            'pmable': False
        }
        self.db = plugin.db
        self.music = plugin.music
        self.cooldown = plugin.cooldown
        self.log = plugin.log
        self.bot = plugin.bot
        self.plugin = plugin

        try:
            self.load_info(info)
        except NotEnabledError:
            return

    def load_info(self, info):
        if 'enabled' in info and info['enabled']:
            self.enabled = True
        else:
            raise NotEnabledError

        self.name = info['name']
        self.path = self.plugin.path

        if 'usage' in info:
            self.usage = info['usage']

        if 'description' in info:
            self.desc = info['description']

        for key in ['global', 'sfw', 'admin', 'partner', 'pmable']:
            if key in info:
                self.perm[key] = info[key]

        module_path = os.path.join(self.path, self.name)
        self.modpath = module_path.replace('/', '.').replace('\\', '.')
        self.module = import_module(self.modpath)

    def resource(self, what):
        res = os.path.join(self.path, 'res', what)

        if os.path.exists(res):
            return res

        return global_resource(what)

    @classmethod
    def help(cls):
        return ''

    async def call(self, message, *args):
        server = message.guild
        channel = message.channel
        author = message.author

        if author.bot:
            return

        perm = check_permitted(self, author, channel, server)

        if not perm[0]:
            try:
                await channel.send(embed=perm[1])
            except:
                pass
            return

        try:
            await getattr(self.module, self.name)(self, message, *args)
        except exception as e:
            try:
                title = '❗ An Error Occurred!'
                errmsg = 'For more information you can go to the AP Discord server and ask us, '
                errmsg += 'the link is in the help.'
                self.log.error(f'CMD: {self.name} | ERROR: {e} | TRACE: {e.with_traceback}')
                error_embed = discord.Embed(color=0xDB0000)
                error_embed.add_field(name=title,
                                      value=codeblock(f'Arguments: \"{e}\"\nTraceback: \"{e.with_traceback}\"'))
                error_embed.set_footer(text=errmsg)
                await channel.send(None, embed=error_embed)
            except:
                pass

    async def call_sp(self, member):
        try:
            await getattr(self.module, self.name)(self, member)
        except exception as e:
            # ev_log_msg = f'SP_EV: {member.guild.name} [{member.guild.id}] | {self.name} |'
            # ev_log_msg += f'ERROR: {e} | TRACE: {e.with_traceback}'
            # self.log.error(ev_log_msg)
            pass

    async def call_ready(self):
        try:
            await getattr(self.module, self.name)(self)
        except exception as e:
            self.log.error(f'RD_EV: {self.name} | ERROR: {e} | TRACE: {e.with_traceback}')

    async def call_message_edit(self, before, after):
        try:
            await getattr(self.module, self.name)(self, before, after)
        except exception as e:
            self.log.error(f'RD_EV: {self.name} | ERROR: {e} | TRACE: {e.with_traceback}')

    async def call_voice_update(self, member, before, after):
        if not member.bot:
            try:
                await getattr(self.module, self.name)(self, member, before, after)
            except:
                pass
