# Utilities
from .utils.help import Help
from .utils.echo import Echo
from .utils.nsfwperms import NSFWPermission
from .utils.utils import MakeCommandList
from .utils.utils import Reminder
from .utils.utils import Donators
from .utils.utils import OtherUtils
from .utils.utils import BulkMSG
from .utils.utils import SetAvatar
from .utils.utils import PMRedirect
from .utils.weather import Weather
from .utils.github import GitHub
# Game Related
from .games.league import LeagueOfLegends
from .games.bns import BladeAndSoul
from .games.osu import OSU
from .games.overwatch import Overwatch
from .games.hearthstone import Hearthstone
from .games.pokemon import Pokemon
from .games.vindictus import VindictusScrollSearch
from .games.world_of_warcraft import World_Of_Warcraft
from .games.rocket_league import RocketLeague
from .games.magic import MagicTheGathering
from .games.wargaming.wows import WorlfOfWarships
from .games.wargaming.wot import WorldOfTanks
# Search and Media
from .searches.urbandictionary import UrbanDictionary
from .searches.lastfm import LastFM
from .searches.isthereanydeal import ITAD
from .searches.imdb import IMDB
from .searches.mal import MAL
from .searches.sonarr import Sonarr
from .searches.vndb import VNDBSearch
from .searches.imgur import Imgur
from .searches.reddit import Reddit
from .searches.awwnime import Awwnime
# NSFW Modules
from .nsfw.gelbooru import Gelbooru
from .nsfw.r34 import R34
from .nsfw.nhentai import NHentai
from .nsfw.ehentai import EHentai
from .nsfw.e621 import E621
from .nsfw.hentaims import HentaiMS
from .nsfw.key_vis import KeyVisual
# Japanese Learning and Specific Modules
from .nihongo.wanikani import WK
from .nihongo.wanikani import WKKey
from .nihongo.jisho import Jisho
# Final Order Specific Modules
from .finalo.karaoke import VoiceChangeDetection
from .finalo.karaoke import Control
from .finalo.selfrole import SelfRole
# Miscellaneous
from .misc.joke import Joke
from .misc.rip import Rip
from .misc.reward import RewardOnMessage
from .misc.reward import LevelCheck
from .misc.unflip import Table
from .misc.cleverbot import Cleverbot


__all__ = [
    'Help',
    'LeagueOfLegends',
    'BladeAndSoul',
    'OSU',
    'UrbanDictionary',
    'Weather',
    'Hearthstone',
    'Pokemon',
    'Joke',
    'Overwatch',
    'Rip',
    'LastFM',
    'Echo',
    'NSFWPermission',
    'Gelbooru',
    'R34',
    'NHentai',
    'EHentai',
    'E621',
    'HentaiMS',
    'ITAD',
    'IMDB',
    'WK',
    'WKKey',
    'Jisho',
    'MAL',
    'VindictusScrollSearch',
    'Sonarr',
    'VoiceChangeDetection',
    'Control',
    'VNDBSearch',
    'Reminder',
    'Donators',
    'OtherUtils',
    'BulkMSG',
    'Imgur',
    'RewardOnMessage',
    'LevelCheck',
    'PMRedirect',
    'SelfRole',
    'World_Of_Warcraft',
    'RocketLeague',
    'SetAvatar',
    'Reddit',
    'Table',
    'Cleverbot',
    'MagicTheGathering',
    'KeyVisual',
    'WorlfOfWarships',
    'WorldOfTanks',
    'MakeCommandList',
    'GitHub',
    'Awwnime'
]
