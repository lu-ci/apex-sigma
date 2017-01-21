from cleverbot import Cleverbot

cb = Cleverbot('Apex-Sigma')


async def cleverbot_control(ev, message, args):
    active = ev.db.get_settings(message.server.id, 'CleverBot')
    if active:
        mention = '<@' + ev.bot.user.id + '>'
        mention_alt = '<@!' + ev.bot.user.id + '>'
        author_id = message.author.id
        if message.content.startswith(mention) or message.content.startswith(mention_alt):
            await ev.bot.send_typing(message.channel)

            if message.content.startswith(mention):
                cb_input = message.content[len(mention) + 1:]
            elif message.content.startswith(mention_alt):
                cb_input = message.content[len(mention_alt) + 1:]
            else:
                return
            response = cb.ask(cb_input)
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
