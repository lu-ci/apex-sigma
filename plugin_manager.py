from plugin import Plugin

from plugins.help import Help
from plugins.league import LeagueOfLegends
from plugins.bns import BladeAndSoul
from plugins.osu import OSU
from plugins.urbandictionary import UrbanDictionary
from plugins.weather import Weather
from plugins.hearthstone import Hearthstone
from plugins.pokemon import Pokemon
from plugins.joke import Joke
from plugins.overwatch import Overwatch
from plugins.rip import Rip
from plugins.lastfm import LastFM
from plugins.echo import Echo
from plugins.nsfwperms import NSFWPermission
from plugins.gelbooru import Gelbooru
from plugins.r34 import R34
from plugins.nhentai import NHentai
from plugins.ehentai import EHentai
from plugins.e621 import E621
from plugins.hentaims import HentaiMS
from plugins.isthereanydeal import ITAD
from plugins.imdb import IMDB
from plugins.nihongo import WK
from plugins.nihongo import WKKey
from plugins.jisho import Jisho
from plugins.mal import MAL
from plugins.vindictus import VindictusScrollSearch
from plugins.sonarr import Sonarr
from plugins.karaoke import VoiceChangeDetection
from plugins.karaoke import Control
from plugins.vndb import VNDBSearch
from plugins.utils import Reminder
from plugins.utils import Donators
from plugins.utils import OtherUtils
from plugins.utils import BulkMSG
from plugins.imgur import Imgur
from plugins.reward import RewardOnMessage
from plugins.reward import LevelCheck
from plugins.utils import PMRedirect
from plugins.selfrole import SelfRole
from plugins.world_of_warcraft import World_Of_Warcraft
from plugins.rocket_league import RocketLeague
from plugins.utils import SetAvatar
from plugins.reddit import Reddit
from plugins.unflip import Table
from plugins.cleverbot import Cleverbot
from plugins.magic import MagicTheGathering
from plugins.github import GitHub


class PluginManager:
    def __init__(self, client):
        self.client = client
        self.client.plugins = []

    def load(self, plugin):
        print('Plugin Manager: Loading Plugin: [ ' + plugin.__name__ + ' ]')
        plugin_instance = plugin(self.client)
        self.client.plugins.append(plugin_instance)

    def load_all(self):
        n = 0
        print('\nPlugin Manager: Starting Mass Plugin Load\n')
        for plugin in Plugin.plugins:
            self.load(plugin)
            n += 1
        print('\nFinished Mass Plugin Load\nTotal Plugins Loaded: ' + str(n) + '\n')

    async def get_all(self):
        plugins = []
        for plugin in self.client.plugins:
            if plugin.is_global:
                plugins.append(plugin)
                # if plugin.__class__.__name__ in plugin_names:
                #    plugins.append(plugin)
        return plugins
