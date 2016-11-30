import asyncio
from cleverbot import Cleverbot

cb = Cleverbot()


async def cleverbot(ev, message, args):
    mention = '<@' + ev.bot.user.id + '>'
    mention_alt = '<@!' + ev.bot.user.id + '>'
    author_id = message.author.id
    if message.content.startswith(mention) or message.content.startswith(mention_alt):
        await ev.bot.send_typing(message.channel)

        try:
            if message.content.startswith(mention):
                cb_input = message.content[len(mention) + 1:]
            elif message.content.startswith(mention_alt):
                cb_input = message.content[len(mention_alt) + 1:]
            else:
                return
            response = cb.ask(cb_input)
            await asyncio.sleep(len(response) * 0.0145)
            await ev.bot.send_message(message.channel, '<@' + message.author.id + '> ' + response)
            find_data = {
                'Role': 'Stats'
            }
            find_res = ev.db.find('Stats', find_data)
            count = 0
            for res in find_res:
                try:
                    count = res['CBCount']
                except:
                    count = 0
            new_count = count + 1
            updatetarget = {"Role": 'Stats'}
            updatedata = {"$set": {"CBCount": new_count}}
            ev.db.update_one('Stats', updatetarget, updatedata)
        except Exception as e:
            ev.log.error(e)
            msg = 'Sorry <@{:s}>, my brain isn\'t working at the moment give me some time to catch my breath...'
            await ev.bot.send_message(message.channel, msg.format(author_id))
