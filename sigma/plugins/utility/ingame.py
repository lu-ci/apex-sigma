import discord
import operator


async def ingame(cmd, message, args):
    games = {}
    online_count = 0
    playing_count = 0
    total_count = 0
    for member in message.server.members:
        total_count += 1
        status = str(member.status)
        if status != 'offline':
            online_count += 1
        if not member.bot:
            if member.game:
                game_name = str(member.game)
                repl_name = game_name.replace(' ', '')
                if repl_name != '':
                    playing_count += 1
                    if game_name not in games:
                        games.update({game_name: 1})
                    else:
                        curr_count = games[game_name]
                        new_count = curr_count + 1
                        games.update({game_name: new_count})
    embed = discord.Embed(color=0x1ABC9C)
    sorted_games = sorted(games.items(), key=operator.itemgetter(1))
    n = 0
    out = ''
    game_count = len(sorted_games)
    for key, value in reversed(sorted_games):
        if n < 5:
            out += '\n**' + key + '**\n - ' + str(value) + ' Playing | ' + \
                   str(((value / game_count) * 10000) // 100).split('.')[
                       0] + '%'
            n += 1
    embed.add_field(name='Current Gaming Statistics on ' + message.server.name, value=out, inline=True)
    embed.set_footer(text=str(playing_count) + ' members, out of ' + str(online_count) + ' online, are playing ' + str(
        game_count) + ' different games.')
    await cmd.bot.send_message(message.channel, None, embed=embed)
