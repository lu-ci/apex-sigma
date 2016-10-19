from .urbandictionary import UrbanDictionary
from .lastfm import LastFM
from .isthereanydeal import ITAD
from .imdb import IMDB
from .mal import MAL
from .sonarr import Sonarr
from .vndb import VNDBSearch
from .imgur import Imgur
from .reddit import Reddit
from .wikipedia import Wikipedia


__all__ = [
    'UrbanDictionary',
    'LastFM',
    'ITAD',
    'IMDB',
    'MAL',
    'Sonarr',
    'VNDBSearch',
    'Imgur',
    'Reddit',
    'Wikipedia'
]

pluglist = __all__
