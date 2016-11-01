import random


async def unflip(ev, message, args):
    if '(╯°□°）╯︵ ┻━┻' in message.content:
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

        await ev.reply(random.choice(table))
