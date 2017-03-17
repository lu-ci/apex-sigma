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
            'donor': False,
            'pmable': False
        }

        self.db = plugin.db
        self.music = plugin.music
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

        for key in ['global', 'sfw', 'admin', 'donor', 'pmable']:
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
        server = message.server
        channel = message.channel
        author = message.author
        msg = None

        if author.bot:
            return

        perm = check_permitted(self, author, channel, server)

        if not perm[0]:
            await self.bot.send_message(channel, embed=perm[1])
            return

        try:
            msg = await getattr(self.module, self.name)(self, message, *args)
        except exception as e:
            try:
                title = ':exclamation: An Error Occurred!'
                errmsg = 'For more information you can go to the AP Discord server and ask us, '
                errmsg += 'the link is in the help.'
                self.log.error(f'CMD: {self.name} | ERROR: {e} | TRACE: {e.with_traceback}')
                error_embed = discord.Embed(color=0xDB0000)
                error_embed.add_field(name=title,
                                      value=codeblock(f'Arguments: \"{e}\"\nTraceback: \"{e.with_traceback}\"'))
                error_embed.set_footer(text=errmsg)
                await self.bot.send_message(channel, None, embed=error_embed)
            except:
                pass

        if not self.perm['sfw']:
            self.db.add_stats('NSFWCount')

        if msg:
            await self.bot.send_message(channel, msg)

    async def call_sp(self, member):
        try:
            await getattr(self.module, self.name)(self, member)
        except Exception as e:
            self.log.error(f'EV: {self.name} | ERROR: {e} | TRACE: {e.with_traceback}')

    async def call_ready(self):
        try:
            await getattr(self.module, self.name)(self)
        except Exception as e:
            self.log.error(f'EV: {self.name} | ERROR: {e} | TRACE: {e.with_traceback}')
