import discord


async def volume(cmd, message, args):
    if args:
        if not message.author.voice_channel:
            embed = discord.Embed(
                title='⚠ I don\'t see you in a voice channel', color=0xFF9900)
            await cmd.bot.send_message(message.channel, None, embed=embed)
            return
        try:
            new_vol = int(args[0])
            bad_data = False
        except:
            bad_data = True
            new_vol = 0
        if bad_data or 1 > new_vol > 200:
            embed = discord.Embed(
                title='⚠ Please use a number between 1 and 200.', color=0xFF9900)
            await cmd.bot.send_message(message.channel, None, embed=embed)
            return
        else:
            curr_vol = cmd.music.get_volume(cmd.db, message.server.id)
            player = cmd.music.get_player(message.server.id)
            player.volume = new_vol / 100
            cmd.music.set_volume(cmd.db, message.server.id, new_vol)
            embed = discord.Embed(color=0x696969, title=':loud_sound: Volume Changed')
            embed.add_field(name='New', value=f'```py\n{new_vol}\n```', inline=True)
            embed.add_field(name='Old', value=f'```\n{curr_vol}\n```', inline=True)
            await cmd.bot.send_message(message.channel, None, embed=embed)
    else:
        curr_vol = cmd.music.get_volume(cmd.db, message.server.id)
        embed = discord.Embed(color=0x696969)
        embed.add_field(name=':loud_sound: Current Volume', value=f'```\n{curr_vol}\n```')
        await cmd.bot.send_message(message.channel, None, embed=embed)
