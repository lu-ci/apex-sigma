import random
import discord

async def coinflip(cmd, message, args):
    result = random.choice(['heads', 'tails'])
    urls = {
        'heads': 'https://i.imgur.com/UbsozEv.png',
        'tails': 'https://i.imgur.com/TUraKTb.png'
    }
    embed = discord.Embed(color=0x1abc9c)
    if args:
        choice = args[0]
        if choice.lower().startswith('t') or choice.lower().startswith('h'):
            if choice.lower().startswith('t'):
                choice = 'tails'
            else:
                choice = 'heads'
            if result == choice.lower():
                out = ':ballot_box_with_check: Nice guess!'
            else:
                out = ':regional_indicator_x: Better luck next time!'
            embed = discord.Embed(color=0x1abc9c, title=out)
        else:
            embed.set_footer(text='If you\'re going to guess, guess with Heads or Tails.')
    embed.set_image(url=urls[result])
    await message.channel.send(None, embed=embed)
