from sigma.core.utils import user_avatar
from config import Prefix
import discord
import arrow


async def reminders(cmd, message, args):
    all_reminders = cmd.db.find('Reminders', {'UserID': message.author.id})
    reminder_list = []
    for reminder in all_reminders:
        reminder_list.append(reminder)
    rem_count = len(reminder_list)
    if rem_count != 0:
        if args:
            choice = reminder_list[int(args[0])]
            creation_stamp = arrow.get(choice['CreationStamp'])
            creation_human = creation_stamp.humanize(arrow.utcnow())
            creation_date = creation_stamp.format('YYYY-MM-DD HH:mm:ss')
            execution_stamp = arrow.get(choice['ExecutionStamp'])
            execution_human = execution_stamp.humanize(arrow.utcnow())
            execution_date = execution_stamp.format('YYYY-MM-DD HH:mm:ss')
            response = discord.Embed(color=0x696969)
            response.set_author(name='🕙 Reminder Information', icon_url=user_avatar(message.author))
            response.add_field(name='Created', value=f'{creation_human.title()}\n{creation_date} UTC', inline=True)
            response.add_field(name='Executes', value=f'{execution_human.title()}\n{execution_date} UTC', inline=True)
            response.add_field(name='Message', value=f'{choice["TextMessage"]}', inline=False)
            response.set_footer(text=f'ReminderID: {choice["ReminderID"]}')
        else:
            response = discord.Embed(color=0x0099FF)
            rem_list_out = ''
            for rem in reminder_list:
                exec_time = arrow.get(rem['ExecutionStamp'])
                human_time = exec_time.humanize(arrow.utcnow())
                rem_text = f'**{rem["TextMessage"]}**\n  - {human_time}'
                rem_list_out += f'\n{rem_text}'
            response.add_field(name=f'ℹ Reminder Data', value=f'You have {rem_count} pending reminders.', inline=False)
            response.add_field(name='Upcoming Reminders', value=f'{rem_list_out}', inline=False)
            response.set_footer(text=f'To see their details type {Prefix}reminders [0-{rem_count - 1}]')
    else:
        response = discord.Embed(color=0x696969, title='🔍 You have not made any reminders.')
    await message.channel.send(embed=response)
