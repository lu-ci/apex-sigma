blackjack_instances = {}
symbols = ['♥', '♠', '♣', '♦']
suits = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']


def get_bj(inid):
    if inid in blackjack_instances:
        return blackjack_instances[inid]
    else:
        return None


def add_bj(inid, instance_data):
    global blackjack_instances
    if inid not in blackjack_instances:
        blackjack_instances.update(instance_data)
    else:
        raise KeyError


def del_bj(inid):
    global blackjack_instances
    if inid in blackjack_instances:
        del blackjack_instances[inid]
    else:
        raise KeyError


def upd_bj(inid, new_data):
    global blackjack_instances
    if inid in blackjack_instances:
        blackjack_instances.update(new_data)
    else:
        raise KeyError
