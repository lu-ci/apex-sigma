import discord
from .response_grabber import grab_response
from .targetting import get_target


async def pout(cmd, message, args):
    resp = grab_response(cmd.resource('responses.yml'), 'pout')
    target = get_target(message, args)
    if not target or target.id == message.author.id:
        response = discord.Embed(color=0x1ABC9C, title=f'{message.author.name} pouts.')
    else:
        response = discord.Embed(color=0x1ABC9C, title=f'{message.author.name} pouts at {target.name}.')
    response.set_image(url=resp['url'])
    response.set_footer(text=f'Submitted by {resp["auth"]} from {resp["srv"]}.')
    await message.channel.send(embed=response)
