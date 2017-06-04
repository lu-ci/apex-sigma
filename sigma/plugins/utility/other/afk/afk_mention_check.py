import arrow
import discord
from config import Prefix

async def afk_mention_check(ev, message, args):
    if message.guild:
        if not message.content.startswith(Prefix):
            if message.mentions:
                target = message.mentions[0]
                afk_data = ev.db.find_one('AwayUsers', {'UserID': target.id})
                if afk_data:
                    time_then = arrow.get(afk_data['Timestamp'])
                    afk_time = arrow.get(time_then).humanize(arrow.utcnow()).title()
                    response = discord.Embed(color=0x0099FF, timestamp=time_then.datetime)
                    response.add_field(name=f'ℹ {target.name} is afk!',
                                       value=f'Reason: {afk_data["Reason"]}\nWent AFK: {afk_time}')
                    await message.channel.send(embed=response)
