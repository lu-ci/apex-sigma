import discord


def get_target(message, args):
    if message.mentions:
        target = message.mentions[0]
    else:
        if args:
            lookup = ' '.join(args)
            target = discord.utils.find(lambda x: x.name.lower() == lookup.lower(), message.guild.members)
            if not target:
                target = discord.utils.find(lambda x: x.nickname.lower() == lookup.lower(), message.guild.members)
        else:
            target = None
    return target
