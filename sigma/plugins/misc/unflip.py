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
        find_data = {
            'Role': 'Stats'
        }
        find_res = ev.db.find('Stats', find_data)
        count = 0
        for res in find_res:
            try:
                count = res['TableCount']
            except:
                count = 0
        new_count = count + 1
        updatetarget = {"Role": 'Stats'}
        updatedata = {"$set": {"TableCount": new_count}}
        ev.db.update_one('Stats', updatetarget, updatedata)
        await ev.bot.send_message(message.channel, random.choice(table))
