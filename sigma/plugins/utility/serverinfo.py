import discord


async def serverinfo(cmd, message, args):
    out_list = []
    if message.guild:
        bot_count = 0
        user_count = 0
        serv = message.guild
        for user in serv.members:
            if user.bot:
                bot_count += 1
            else:
                user_count += 1
        out_list.append(['Name', serv.name])
        out_list.append(['Server ID', serv.id])
        out_list.append(['Created', serv.created_at])
        out_list.append(['Default Channel', '#' + serv.default_channel.name])
        out_list.append(['Member Count', str(user_count) + ' (+' + str(bot_count) + ' bots)'])
        out_list.append(['Owner', serv.owner])
        out_list.append(['Owner ID', serv.owner_id])
        out_list.append(['Region', serv.region])
        out_list.append(['Verification Level', serv.verification_level])
        out_list.append(['MFA Level', serv.mfa_level])
        if serv.afk_channel:
            out_list.append(['AFK Channel', serv.afk_channel])
            out_list.append(['AFK Timeout', serv.afk_timeout])
        embed = discord.Embed(title=serv.name + ' Information', color=0x1ABC9C)
        for item in out_list:
            embed.add_field(name=str(item[0]), value='```python\n' + str(item[1]) + '\n```')

        await message.channel.send(None, embed=embed)
