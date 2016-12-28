import discord


async def channelinfo(cmd, message, args):
    if message.channel:
        out_list = []
        n = 0
        nsfw = False
        chan = message.channel
        nsfw_check = cmd.db.find('NSFW', {'ChannelID': chan.id})
        for result in nsfw_check:
            n += 1
            if n > 0:
                nsfw = result['Permitted']
            else:
                nsfw = False
        out_list.append(['Name', chan.name])
        out_list.append(['Channel ID', chan.id])
        out_list.append(['Created', chan.created_at])
        out_list.append(['Is Default', chan.is_default])
        out_list.append(['Is Private', chan.is_private])
        out_list.append(['Position', chan.position])
        out_list.append(['Type', chan.type])
        if chan.topic:
            topic = chan.topic
        else:
            topic = 'None'
        out_list.append(['Topic', topic])
        out_list.append(['NSFW Enabled', nsfw])
        embed = discord.Embed(title='#' + chan.name + ' Information', color=0x1ABC9C)
        for item in out_list:
            embed.add_field(name=str(item[0]), value='```python\n' + str(item[1]) + '\n```')

        await cmd.bot.send_message(message.channel, None, embed=embed)
