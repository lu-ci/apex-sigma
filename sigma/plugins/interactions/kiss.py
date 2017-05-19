import discord
from .response_grabber import grab_response
from .targetting import get_target


async def kiss(cmd, message, args):
    resp = grab_response(cmd.resource('responses.yml'), 'kiss')
    target = get_target(message, args)
    if not target or target.id == message.author.id:
        response = discord.Embed(color=0x1ABC9C, title=f'{message.author.name} tries to kiss themself.')
    else:
        response = discord.Embed(color=0x1ABC9C, title=f'{message.author.name} kisses {target.name}.')
    response.set_image(url=resp['url'])
    response.set_footer(text=f'Submitted by {resp["auth"]} from {resp["srv"]}.')
    await message.channel.send(embed=response)
