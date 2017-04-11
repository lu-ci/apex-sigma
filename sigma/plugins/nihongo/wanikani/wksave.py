import discord


async def wksave(cmd, message, args):
    coll = 'WaniKani'
    try:
        await message.delete()
    except Exception as e:
        cmd.log.error(e)
        cmd.log.info('Message in private channel, unable to delete...')

    user_id = int(message.author.id)

    try:
        mode = args.pop(0)
        payload = ' '.join(args)

        if not mode:
            embed = discord.Embed(color=0xDB0000, title='❗ No mode was inputted.')
            await message.channel.send(None, embed=embed)
            return
        if mode not in ['key', 'username', 'remove']:  # remove
            embed = discord.Embed(color=0xDB0000, title='❗ Unknown Argument.')
            await message.channel.send(None, embed=embed)
            return
        if mode == 'key':
            if len(payload) < 32 or len(payload) > 32:
                embed = discord.Embed(color=0xDB0000, title='❗ The key seems invalid.')
                await message.channel.send(None, embed=embed)
                return

        if mode == 'remove':  # remove
            query = {'UserID': user_id}
            cmd.db.delete_one(coll, query)

            embed = discord.Embed(color=0xDB0000, title=':x: Record deleted.')
            await message.channel.send(None, embed=embed)
            return

        if mode == 'key':
            insert_query = {
                'UserID': user_id,
                'WKAPIKey': payload,
                'WKUsername': None
            }
            update_query = {'$set': {
                'WKAPIKey': payload,
                'WKUsername': None
            }}
        elif mode == 'username':
            insert_query = {
                'UserID': user_id,
                'WKAPIKey': None,
                'WKUsername': payload
            }
            update_query = {'$set': {
                'WKAPIKey': None,
                'WKUsername': payload
            }}
        else:
            return

        n = 0
        check_exist_qry = {'UserID': user_id}
        find_res = cmd.db.find(coll, check_exist_qry)
        for result in find_res:
            n += 1
        if n == 0:
            cmd.db.insert_one(coll, insert_query)
            embed = discord.Embed(color=0x0099FF, title=':key: ' + mode.capitalize() + ' Safely Stored.')
            await message.channel.send(None, embed=embed)
        else:
            update_target = {'UserID': user_id}
            cmd.db.update_one(coll, update_target, update_query)
            embed = discord.Embed(color=0x0099FF, title=':key: ' + mode.capitalize() + ' Updated.')
            await message.channel.send(None, embed=embed)
    except Exception as e:
        cmd.log.error(e)
        embed = discord.Embed(color=0xDB0000, title='❗ Error while parsing the input message.')
        await message.channel.send(None, embed=embed)
