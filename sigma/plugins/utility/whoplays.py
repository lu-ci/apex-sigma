import discord


async def whoplays(cmd, message, args):
    if not args:
        await message.channel.send(cmd.help())
        return
    else:
        game_title = ' '.join(args)
        gamer_list = ''
        x = 0
        y = 0
        for member in message.guild.members:
            if member.game:
                x += 1
                if str(member.game).lower() == game_title.lower():
                    y += 1
                    gamer_list += member.name + ', '
        gamer_list = gamer_list[:-2]
        if gamer_list == '':
            gamer_list = 'None'
        point = 'are'
        if y == 1:
            point = 'is'
        title = 'Out of ' + str(x) + ' people that ' + point + ' currently in-game, ' + str(
            y) + ' are playing ' + game_title + ':'
        gamers = '```\n' + gamer_list + '\n```'
        embed = discord.Embed(color=0x1ABC9C)
        embed.add_field(name=title, value=gamers)
        await message.channel.send(None, embed=embed)
