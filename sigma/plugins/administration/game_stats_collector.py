import asyncio


async def game_stats_collector(ev):
    while True:
        if not ev.db.on_cooldown('Sigma', 'Sigma', 'GameStatsCollector', 3600):
            ev.db.set_cooldown('Sigma', 'Sigma', 'GameStatsCollector')
            games = {}
            online_count = 0
            playing_count = 0
            total_count = 0
            for member in ev.bot.get_all_members():
                total_count += 1
                status = str(member.status)
                if status != 'offline':
                    online_count += 1
                if not member.bot:
                    if member.game:
                        try:
                            game_name = str(member.game)
                            repl_name = game_name.replace(' ', '')
                            if repl_name != '':
                                game_name = game_name.replace('.', '').replace(',', '').replace(' ', '_').lower()
                                playing_count += 1
                                if game_name not in games:
                                    games.update({game_name: 1})
                                else:
                                    curr_count = games[game_name]
                                    new_count = curr_count + 1
                                    games.update({game_name: new_count})
                        except:
                            pass
            payload = {
                'games': games,
                'online': online_count,
                'playing': playing_count,
                'total': total_count
            }
            ev.db.insert_one('GameStatistics', payload)
        await asyncio.sleep(300)
