from config import permitted_id


async def inviteowner(cmd, message, args):
    if message.author.id in permitted_id:
        if args:
            server_id_lookup = args[0]
            for server in cmd.bot.servers:
                if server.id == server_id_lookup:
                    try:
                        invite = await cmd.bot.create_invite(server, max_uses=1)
                        await cmd.bot.send_message(message.channel,
                                                   'Invite link to **' + server.name + '**: ' + str(invite))
                    except Exception as e:
                        invs = await cmd.bot.invites_from(server)
                        inv_out = ''
                        for inv in invs:
                            inv_out += '\n' + str(inv)
                        if inv_out == '':
                            return
                        else:
                            await message.channel.send(inv_out)
