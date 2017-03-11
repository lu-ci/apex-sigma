import discord
import random
from config import Prefix


translation = {
    'a1': 0, 'b1': 1, 'c1': 2,
    'a2': 3, 'b2': 4, 'c2': 5,
    'a3': 6, 'b3': 7, 'c3': 8,
}


async def tictactoe(cmd, message, args):
    if args:
        if args[0].lower() == 'start':
            pass
