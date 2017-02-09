import asyncio
import discord

self_roles = ['Dragon Nest', 'PvP [DN]', '4v4 [DN]', 'Wipeout [DN]', 'Guild Rumble [DN]', 'Protect [DN]', 'PvE [DN]',
              'Raids [DN]', 'Nests [DN]', 'Dailies [DN]', 'Starlight [DN]',
              'Blade and Soul', 'PvP [BNS]', 'PvE [BNS]',
              'League of Legends', 'NA [LoL]', 'EU [LoL]', 'OCE [LoL]',
              'Vindictus', 'PvP [Vindi]', 'PvE [Vindi]',
              'Overwatch', 'CS:GO',
              'Black Desert Online', 'PvE [BD]', 'PvP [BD]',
              'Revelation Online', 'PvE [Rev]', 'PvP [Rev]',
              'Team Instinct', 'Team Valor', 'Team Mystic', 'Pokémon',
              'Artists', 'Streamers', 'Entertainers ✿', 'Coders', 'Cosplayers',
              'Welcome Party', 'Cake Shop', 'Weebs',
              'Singers', 'Instrumentalists', 'Showtime', 'Writers',
              'Connect', 'Musical', 'Engage',
              'PST', 'EST', 'UTC', 'CST', 'CET']
timeout = 10


async def selfrole(ev, message, args):
    if message.channel.id == '222882496113672193':
        if message.content == 'Pokemon':
            message.content = 'Pokémon'
        if message.content == 'Entertainers':
            message.content = 'Entertainers ✿'
        if message.author.id == ev.bot.user.id:
            pass
        else:
            await ev.bot.delete_message(message)

        if message.content in self_roles:  # if message has the correct keyword
            user_has_role = False
            for role in message.author.roles:
                if role.name == message.content:
                    if role.name in self_roles:  # if user has a role
                        user_has_role = True
                        break

            for role in message.server.roles:
                if role.name == message.content:
                    if user_has_role:
                        await ev.bot.remove_roles(message.author, role)
                        embed = discord.Embed(
                            title=':warning: ' + role.name + ' has been removed from you as you already had it.',
                            color=0xFF9900)
                        response = await ev.bot.send_message(message.channel, None, embed=embed)
                        await asyncio.sleep(timeout)
                        await ev.bot.delete_message(response)

                        return
                    else:
                        await ev.bot.add_roles(message.author, role)
                        embed = discord.Embed(title=':white_check_mark: ' + role.name + ' has been added to you.',
                                              color=0x66cc66)
                        response = await ev.bot.send_message(message.channel, None, embed=embed)

                        await asyncio.sleep(timeout)
                        await ev.bot.delete_message(response)

                        return
