from .slot_core import spin_slots


async def slots(cmd, message, args):
    cost = 10
    if args:
        try:
            cost = abs(int(args[0]))
        except:
            pass
    symbols = [':sunny:', ':crescent_moon:', ':eggplant:', ':gun:', ':diamond_shape_with_a_dot_inside:', ':bell:',
               ':maple_leaf:', ':musical_note:', ':gem:', ':fleur_de_lis:', ':trident:', ':knife:', ':fire:',
               ':clown:', ':radioactive:', ':green_heart:', ':telephone:', ':hamburger:', ':banana:',
               ':tumbler_glass:']
    await spin_slots(cmd, message, cost, symbols)
