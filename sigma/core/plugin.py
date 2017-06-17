import os
import yaml
from itertools import dropwhile

from .command import Command
from .event import Event
from .logger import create_logger


class PluginNotEnabled(RuntimeError):
    pass


class Plugin(object):
    def __init__(self, bot, path):
        self.loaded = False
        self.help = 'No help available, sorry :('
        self.commands_info = []
        self.events_info = []

        self.commands = {}
        self.events = {
            'mention': {},
            'message': {},
            'member_join': {},
            'member_leave': {},
            'ready': {},
            'voice_update': {},
            'message_edit': {}
        }
        self.modules = []
        self.path = path

        self.db = bot.db
        self.music = bot.music
        self.cooldown = bot.cooldown
        self.bot = bot

        try:
            self.load_info(bot)
        except PluginNotEnabled:
            return

        self.load_events()
        self.load_commands()
        self.loaded = True
        self.log.info('Loaded plugin {:s}'.format(self.name))

    def load_info(self, bot):
        with open(os.path.join(self.path, 'plugin.yml')) as yml_file:
            yml = yaml.safe_load(yml_file)

            if 'enabled' not in yml or not yml['enabled']:
                raise PluginNotEnabled

            path = self.path.split('/')
            name = path.pop()

            # use the directory as plugin name if it is not set
            if 'name' not in yml:
                yml['name'] = name

            self.name = yml['name']

            self.log = create_logger(self.name)
            self.log.info('Loading plugin {:s}'.format(self.name))

            # set categories from rest of pathname
            if 'categories' not in yml:
                it = iter(path)
                cat = [dropwhile(lambda x: x != 'plugins', it)][1:]
                yml['categories'] = cat

            self.categories = yml['categories']

            if 'commands' in yml:
                self.commands_info = yml['commands']

            if 'events' in yml:
                self.events_info = yml['events']

    def load_commands(self):
        for cmd_info in self.commands_info:
            cmd = Command(self, cmd_info)

            if cmd.enabled:
                self.commands.update({cmd_info['name']: cmd})
                self.modules.append(cmd.module)

        if self.commands:
            self.log.info('Loaded commands: [{:s}]'.format(
                ', '.join(self.commands.keys())))

    def load_events(self):
        for ev_info in self.events_info:
            ev = Event(self, ev_info)

            if ev.enabled:
                self.events[ev.type].update({ev_info['name']: ev})
                self.modules.append(ev.module)

        for ev_type, events in self.events.items():
            if events:
                self.log.info('Loaded {:s} events: [{:s}]'.format(
                        ev_type, ', '.join(events.keys())))
