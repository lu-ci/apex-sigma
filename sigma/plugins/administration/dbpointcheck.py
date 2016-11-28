from config import permitted_id


async def dbpointcheck(cmd, message, args):
    if message.author.id in permitted_id:
        qry = {}
        data = cmd.db.find('PointSystem', qry)
        all_members = cmd.bot.get_all_members()
        n = 0
        for result in data:
            try:
                result['Avatar']
            except:
                for member in all_members:
                    if member.id == result['UserID']:
                        curr_pts = result['Points']
                        level = int(curr_pts / 1690)
                        updatetarget = {"UserID": result['UserID'], "ServerID": result['ServerID']}
                        updatedata = {"$set": {
                            'UserName': member.name,
                            'Avatar': member.avatar_url,
                            'Level': level
                        }}
                        cmd.db.update_one('PointSystem', updatetarget, updatedata)
                        n += 1
        await cmd.bot.send_message(message.channel, 'Done.\nUpdated ' + str(n) + ' missing users.')
