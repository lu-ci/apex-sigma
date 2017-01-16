import random
import discord


async def roll(cmd, message, args):
    if args:
        try:
            endrange = int(args[0])
        except Exception as e:
            cmd.log.error(e)
            embed = discord.Embed(color=0xDB0000, title=':exclamation: Only numbers are accepted for the end range.')
            await cmd.bot.send_message(message.channel, None, embed=embed)
            return
    else:
        endrange = 100
    number = random.randint(1, endrange)
    num = str(number)
    if len(num) > 1950:
        num = num[:1950] + '...'
    embed = discord.Embed(color=0x1abc9c)
    embed.add_field(name='🎲 You Rolled', value='```\n' + num + '\n```')
    await cmd.bot.send_message(message.channel, None, embed=embed)
