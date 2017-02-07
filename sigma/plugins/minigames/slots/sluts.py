from .slot_core import spin_slots


async def sluts(cmd, message, args):
    cost = 10
    if args:
        try:
            cost = abs(int(args[0]))
        except:
            pass
    symbols = [':girl:', ':woman:', ':older_woman:', ':princess:', ':dancer:', ':dancers:', ':ok_woman:', ':virgo:',
               ':cocktail:', ':bride_with_veil:', ':two_women_holding_hands:', ':lips:', ':tongue:', ':high_heel:',
               ':pregnant_woman:', ':couple_ww:', ':bikini:', ':kiss:', ':lipstick:', ':wilted_rose:']
    await spin_slots(cmd, message, cost, symbols)
