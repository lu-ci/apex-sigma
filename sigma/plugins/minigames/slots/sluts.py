from .slot_core import spin_slots


async def sluts(cmd, message, args):
    cost = 10
    if args:
        try:
            cost = abs(int(args[0]))
        except:
            pass
    symbols = ['👧', '👩', '👴', '👸', '💃', '👯', '🙆', '♍', '🍸', '👰',
               '👭', '👄', '👅', '👠', '🤰', '💍', '👙', '💋', '💄', '🥀']
    await spin_slots(cmd, message, cost, symbols)
