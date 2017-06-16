import discord


async def overridelovecalculator(cmd, message, args):
    if args:
        if len(args) == 3:
            if len(message.mentions) == 2:
                collection = 'LoveCalcOverrides'
                override_value = args[0]
                target_one = message.mentions[0]
                target_two = message.mentions[1]
                targets = [target_one.id, target_two.id]
                target_data = {'Targets': targets}
                lookup = cmd.db.find_one(collection, target_data)
                if override_value.lower() == 'disable':
                    if lookup:
                        cmd.db.delete_one(collection, target_data)
                        response = discord.Embed(color=0x66CC66,
                                                 title=f'✅ Removed {target_one.name} and {target_two.name} override.')
                    else:
                        response = discord.Embed(color=0xDB0000, title='❗ No Override Found')
                else:
                    override_value = int(override_value)
                    if override_value < 0:
                        response = discord.Embed(color=0xDB0000, title='❗ Number Too Low')
                    elif override_value > 200:
                        response = discord.Embed(color=0xDB0000, title='❗ Number Too High')
                    else:
                        if lookup:
                            action = 'updated'
                            cmd.db.delete_one(collection, target_data)
                        else:
                            action = 'created'
                        insert_data = {
                            'OverrideValue': override_value,
                            'Targets': targets
                        }
                        cmd.db.insert_one(collection, insert_data)
                        response = discord.Embed(color=0x66CC66,
                                                 title=f'✅ {target_one.name} and {target_two.name} override {action}.')
            else:
                response = discord.Embed(color=0xDB0000, title='❗ Not Enough Mentions')
        else:
            response = discord.Embed(color=0xDB0000, title='❗ Not Enough Arguments')
    else:
        response = discord.Embed(color=0xDB0000, title='❗ No Arguments Given')
    await message.channel.send(embed=response)
