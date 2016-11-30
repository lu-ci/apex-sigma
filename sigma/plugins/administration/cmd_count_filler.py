from config import Prefix

async def cmd_count_filler(ev, message, args):
    if message.content.startswith(Prefix):
        find_data = {
            'Role': 'Stats'
        }
        find_res = ev.db.find('Stats', find_data)
        count = 0
        for res in find_res:
            try:
                count = res['CMDCount']
            except:
                count = 0
        new_count = count + 1
        updatetarget = {"Role": 'Stats'}
        updatedata = {"$set": {"CMDCount": new_count}}
        ev.db.update_one('Stats', updatetarget, updatedata)
