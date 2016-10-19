from .league import LeagueOfLegends
from .bns import BladeAndSoul
from .osu import OSU
from .overwatch import Overwatch
from .hearthstone import Hearthstone
from .pokemon import Pokemon
from .vindictus import VindictusScrollSearch
from .world_of_warcraft import World_Of_Warcraft
from .rocket_league import RocketLeague
from .magic import MagicTheGathering
from .steam import Steam
from . import wargaming

__all__ = [
    'LeagueOfLegends',
    'BladeAndSoul',
    'OSU',
    'Overwatch',
    'Hearthstone',
    'Pokemon',
    'VindictusScrollSearch',
    'World_Of_Warcraft',
    'RocketLeague',
    'Steam',
    'MagicTheGathering',
    'WorldOfWarships',
    'WorldOfTanks'
]

pluglist = __all__
pluglist += wargaming.pluglist
