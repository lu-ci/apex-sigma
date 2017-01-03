from PIL import Image
import os
import discord


async def color(cmd, message, args):
    if not args:
        await cmd.bot.send_message(message.channel, cmd.help())
    else:
        if len(args) == 3:
            for arg in args:
                if int(arg) > 255:
                    await cmd.bot.send_message(message.channel,
                                               'Error processing inputted variables.\nNo number can be greater than 255 when defining RGB.')
                    return
            try:
                clr = (int(args[0]), int(args[1]), int(args[2]))
            except:
                await cmd.bot.send_message(message.channel, 'Error processing inputted variables.')
                return
        else:
            try:
                clr = str(args[0])
                part1 = clr[:2]
                part1 = int(part1, 16)
                part2 = clr[2:-2]
                part2 = int(part2, 16)
                part3 = clr[4:]
                part3 = int(part3, 16)
                clr = (part1, part2, part3)
            except:
                await cmd.bot.send_message(message.channel, 'Error processing inputted variables.')
                return
        img = Image.new('RGB', (50, 50), clr)
        img.save('cache/' + message.author.id + '.png')
        await cmd.bot.send_file(message.channel, 'cache/' + message.author.id + '.png')
        os.remove('cache/' + message.author.id + '.png')
