import discord


async def channelinfo(cmd, message, args):
    if message.channel_mentions:
        chan = message.channel_mentions[0]
    else:
        chan = message.channel
    out_list = []
    n = 0
    nsfw = False
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
    out_list.append(['Is Default', chan.is_default()])
    out_list.append(['Position', chan.position])
    if chan.topic:
        topic = chan.topic
    else:
        topic = 'None'
    out_list.append(['Topic', topic])
    out_list.append(['NSFW Enabled', nsfw])
    embed = discord.Embed(title='#' + chan.name + ' Information', color=0x1ABC9C)
    for item in out_list:
        embed.add_field(name=str(item[0]), value='```python\n' + str(item[1]) + '\n```')
    await message.channel.send(None, embed=embed)
