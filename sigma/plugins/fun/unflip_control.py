import random
from sigma.core.stats import add_special_stats

async def unflip_control(ev, message, args):
    if '(╯°□°）╯︵ ┻━┻' in message.content:
        unflip = True
        if message.guild:
            if ev.db.get_settings(message.guild.id, 'Unflip'):
                unflip = True
        if unflip:
            add_special_stats(ev.db, 'tables_fixed')
            table = ['┬─┬ ノ( ^_^ノ)',
                     '┬─┬ ﾉ(° -°ﾉ)',
                     '┬─┬ ノ(゜-゜ノ)',
                     '┬─┬ ノ(ಠ\_ಠノ)',
                     '┻━┻~~~~  ╯(°□° ╯)',
                     '┻━┻====  ╯(°□° ╯)',
                     '┣ﾍ(^▽^ﾍ)Ξ(ﾟ▽ﾟ*)ﾉ┳━┳ There we go~♪',
                     ' ┬──┬﻿ ¯\_(ツ)',
                     '(ヘ･_･)ヘ┳━┳',
                     'ヘ(´° □°)ヘ┳━┳',
                     '┣ﾍ(≧∇≦ﾍ)… (≧∇≦)/┳━┳']
            await message.channel.send(random.choice(table))
