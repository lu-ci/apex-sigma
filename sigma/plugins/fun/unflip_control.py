import random


async def unflip_control(ev, message, args):
    if '(╯°□°）╯︵ ┻━┻' in message.content:
        unflip = True
        if message.guild:
            if ev.db.get_settings(message.guild.id, 'Unflip'):
                unflip = True
        if unflip:
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
            ev.db.add_stats('TableCount')
            await message.channel.send(random.choice(table))
