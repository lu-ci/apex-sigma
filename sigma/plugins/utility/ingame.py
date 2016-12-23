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
                playing_count += 1
                game_name = str(member.game)
                repl_name = game_name.replace(' ', '')
                if repl_name != '':
                    if game_name not in games:
                        games.update({game_name: 1})
                    else:
                        curr_count = games[game_name]
                        new_count = curr_count + 1
                        games.update({game_name: new_count})
    embed = discord.Embed(title='Top Played Games On ' + message.server.name, color=0x1ABC9C)
    sorted_games = sorted(games.items(), key=operator.itemgetter(1))
    n = 0
    out = ''
    for key, value in reversed(sorted_games):
        if n < 5:
            out += '\n#' + str(n + 1) + ' - **' + key + '** (' + str(value) + ')'
            n += 1
    embed.add_field(name=str(playing_count) + ' Members In Game Out Of ' + str(online_count) + ' Online', value=out)
    await cmd.bot.send_message(message.channel, None, embed=embed)
