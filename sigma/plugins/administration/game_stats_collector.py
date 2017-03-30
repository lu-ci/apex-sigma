import asyncio
import yaml
import os
import arrow

async def game_stats_collector(ev):
    while True:
        if os.path.exists('cache/game_stats_clock.yml'):
            with open('cache/game_stats_clock.yml', 'r') as clock_file:
                clock_data = yaml.safe_load(clock_file)
        else:
            clock_data = {'stamp': 0}
        last_stamp = clock_data['stamp']
        if last_stamp + 3600 < arrow.utcnow().timestamp:
            with open('cache/game_stats_clock.yml', 'w') as clock_file:
                yaml.safe_dump({'stamp': arrow.utcnow().timestamp}, clock_file)
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
                                game_name = ''.join(e for e in game_name if e.isalnum()).replace(' ', '_').lower()
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
                'total': total_count,
                'timestamp': arrow.utcnow().timestamp
            }
            ev.db.insert_one('GameStatistics', payload)
            await asyncio.sleep(3600)
