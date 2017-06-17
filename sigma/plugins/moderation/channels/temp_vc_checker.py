async def temp_vc_checker(ev, member, before, after):
    if before.channel:
        vc = before.channel
        lookup = ev.db.find_one('PrivateRooms', {'ChannelID': vc.id})
        if lookup:
            if len(vc.members) == 0:
                await vc.delete()
                ev.db.delete_one('PrivateRooms', {'ChannelID': vc.id})
