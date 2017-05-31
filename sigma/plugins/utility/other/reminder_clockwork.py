import arrow
import discord
import asyncio
from sigma.core.utils import user_avatar


async def reminder_clockwork(ev):
    while True:
        reminders = ev.db.find('Reminders', {})
        for reminder in reminders:
            current_stamp = arrow.utcnow().timestamp
            execution_stamp = reminder['ExecutionStamp']
            if current_stamp > execution_stamp:
                ev.db.delete_one('Reminders', {'ReminderID': reminder['ReminderID']})
                channel = discord.utils.find(lambda x: x.id == reminder['ChannelID'], ev.bot.get_all_channels())
                author = discord.utils.find(lambda x: x.id == reminder['UserID'], ev.bot.get_all_members())
                if channel:
                    target = channel
                elif author:
                    target = author
                else:
                    target = None
                if target:
                    response = discord.Embed(color=0x1ABC9C, timestamp=arrow.get(reminder['CreationStamp']).datetime)
                    if author:
                        response.set_author(name=author.name, icon_url=user_avatar(author))
                    response.add_field(name='⏰ Reminder Message', value=f"```\n{reminder['TextMessage']}\n```")
                    try:
                        if author:
                            await target.send(author.mention, embed=response)
                        else:
                            await target.send(embed=response)
                    except:
                        pass
        await asyncio.sleep(1)
