import discord


async def blacklist(cmd, message, args):
    black_users = cmd.db.get_settings(message.guild.id, 'BlacklistedUsers')
    black_chnls = cmd.db.get_settings(message.guild.id, 'BlacklistedChannels')
    if not black_chnls and not black_users:
        response = discord.Embed(color=0x0099FF, title='ℹ Nothing Is Blacklisted Here')
    else:
        response = discord.Embed(color=0x1abc9c)
        if black_chnls:
            black_chnls_list = []
            for chnl in black_chnls:
                chnl_name = discord.utils.find(lambda x: x.id == chnl, cmd.bot.get_all_channels()).name
                black_chnls_list.append(chnl_name)
            response.add_field(name='Blacklisted Channels', value=f'```\n{", ".join(black_chnls_list)}\n```')
        if black_users:
            black_users_list = []
            for usr in black_users:
                chnl_name = discord.utils.find(lambda x: x.id == usr, cmd.bot.get_all_members()).name
                black_users_list.append(f'#{chnl_name}')
            response.add_field(name='Blacklisted Users', value=f'```\n{", ".join(black_users_list)}\n```')
    await message.channel.send(None, embed=response)
