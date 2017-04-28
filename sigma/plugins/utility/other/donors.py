import discord
from config import MainServerURL

async def donors(cmd, message, args):
    embed = discord.Embed(color=0x0099FF)
    don_text = f'A **huge** thank you to [these]({MainServerURL}#donors) lovely people!'
    don_text += '\n\nWant to support us?\nWe have a [PayPal.me](https://www.paypal.me/AleksaRadovic) page!'
    embed.add_field(name=':gem: The lovely people that support us', value=don_text)
    embed.set_footer(text='Thank you! 🎀')

    await message.channel.send(None, embed=embed)
