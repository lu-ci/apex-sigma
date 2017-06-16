import discord


async def overriderategirl(cmd, message, args):
    if args:
        collection = 'HotCrazyOverrides'
        if args[0].lower() == 'disable':
            if message.mentions:
                target = message.mentions[0]
                target_data = {'UserID': target.id}
                lookup = cmd.db.find_one(collection, target_data)
                if lookup:
                    cmd.db.delete_one(collection, target_data)
                    response = discord.Embed(color=0x66CC66,
                                             title=f'✅ Removed {target.name} override.')
                else:
                    response = discord.Embed(color=0xDB0000, title='❗ No Override Found')
            else:
                response = discord.Embed(color=0xDB0000, title='❗ No User Mentioned')
        else:
            if len(args) == 3:
                if message.mentions:
                    target = message.mentions[0]
                    target_data = {'UserID': target.id}
                    lookup = cmd.db.find_one(collection, target_data)
                    hot_value = int(args[0])
                    crazy_value = int(args[1])
                    if hot_value < 0 or crazy_value < 0:
                        response = discord.Embed(color=0xDB0000, title='❗ Number Too Low')
                    elif hot_value > 99 or crazy_value > 99:
                        response = discord.Embed(color=0xDB0000, title='❗ Number Too High')
                    else:
                        if lookup:
                            action = 'updated'
                            cmd.db.delete_one(collection, target_data)
                        else:
                            action = 'created'
                        insert_data = {
                            'HotValue': hot_value,
                            'CrazyValue': crazy_value,
                            'UserID': target.id
                        }
                        cmd.db.insert_one(collection, insert_data)
                        response = discord.Embed(color=0x66CC66,
                                                 title=f'✅ {target.name} override {action}.')
                else:
                    response = discord.Embed(color=0xDB0000, title='❗ No User Mentioned')
            else:
                response = discord.Embed(color=0xDB0000, title='❗ Not Enough Arguments')
    else:
        response = discord.Embed(color=0xDB0000, title='❗ No Arguments Given')
    await message.channel.send(embed=response)
