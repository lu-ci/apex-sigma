import discord


async def makeroom(cmd, message, args):
    if args:
        room_name = ' '.join(args)
    else:
        room_name = f'{message.author.name}\'s Room'
    if message.author.voice:
        room_vc = await message.guild.create_voice_channel(room_name)
        await room_vc.edit(position=0)
        await room_vc.edit(bitrate=96000)
        await message.author.move_to(room_vc)
        cmd.db.insert_one('PrivateRooms', {'ChannelID': room_vc.id})
        response = discord.Embed(color=0x66CC66, title=f'✅ `{room_name}` Voice Channel has been created.')
    else:
        response = discord.Embed(color=0xDB0000, title='❗ You you are not in a voice channel.')
    await message.channel.send(embed=response)
