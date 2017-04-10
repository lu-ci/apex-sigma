import discord


async def emojis(cmd, message, args):
    if message.server.emojis:
        emoji_list = []
        for emoji in message.server.emojis:
            emoji_list.append(f'{emoji}')
        emoji_list = ' '.join(emoji_list)[:1950]
        response = discord.Embed(color=0x1ABC9C)
        response.add_field(name=f'😃 Custom Emojis On {message.server.name}', value=emoji_list)
    else:
        response = discord.Embed(color=0x696969, title=f'🔍 No Emojis Found On {message.server.name}')
    await message.channel.send(None, embed=response)
