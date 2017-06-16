import discord


async def lovecalculator(cmd, message, args):
    if message.mentions:
        if len(message.mentions) >= 2:
            id_based = True
            target_1 = message.mentions[0]
            target_2 = message.mentions[1]
        else:
            if len(args) > 1:
                id_based = False
                target_1 = message.mentions[0].name.lower()
                target_2 = args[1].lower()
            else:
                id_based = True
                target_1 = message.author
                target_2 = message.mentions[0]
    elif args:
        id_based = False
        if len(args) >= 2:
            target_1 = args[0].lower()
            target_2 = args[1].lower()
        else:
            target_1 = message.author.name.lower()
            target_2 = args[0].lower()
    else:
        return
    if id_based:
        targets = [target_1.id, target_2.id]
        target_data = {'Targets': targets}
        lookup = cmd.db.find_one('LoveCalcOverrides', target_data)
        if lookup:
            value = lookup['OverrideValue'] // 2
        else:
            mod_1 = int(str(target_1.id)[6] + str(target_1.id)[9])
            mod_2 = int(str(target_2.id)[6] + str(target_2.id)[9])
            value = (mod_1 + mod_2) // 2
    else:
        targets = [target_1, target_2]
        numbers = []
        for target in targets:
            number = 0
            divider = len(target)
            for char in target:
                number += ord(char)
            average = number // divider
            modifier = int((average / number) * 100)
            numbers.append(modifier)
        value = (numbers[0] + numbers[1]) // 2
    bar_len = (value * 2) // 10
    empty_len = 20 - bar_len
    bar_text = f'[{"▚"*bar_len}{"_"*empty_len}]'
    response = discord.Embed(color=0xff6666, title='💝 Love Calculator')
    if id_based:
        first_item = target_1.name
        second_item = target_2.name
    else:
        first_item = target_1.title()
        second_item = target_2.title()
    response.add_field(name='First Item', value=f'```haskell\n{first_item}\n```', inline=True)
    response.add_field(name='Second Item', value=f'```haskell\n{second_item}\n```', inline=True)
    response.add_field(name='Value', value=f'```css\n{bar_text}\n```', inline=False)
    await message.channel.send(embed=response)
