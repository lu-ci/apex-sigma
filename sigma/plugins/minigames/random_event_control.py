import discord
import yaml
import random

events_active = []


async def random_event_control(ev, message, args):
    if message.guild:
        events_enabled = ev.db.get_settings(message.guild.id, 'RandomEvents')
        if events_enabled:
            event_id = message.guild.id + message.author.id
            global events_active
            if event_id in events_active:
                return
            chance = ev.db.get_settings(message.guild.id, 'EventChance')
            rolled_number = random.randint(1, 100)
            if rolled_number <= chance:
                with open(ev.resource('events.yml')) as events_file:
                    event_data = yaml.safe_load(events_file)
                event = random.choice(event_data['events'])
                event_embed = discord.Embed(color=0x1abc9c, title='💠 An event!')
                choice_text_out = ''
                n = 0
                for choice in event['choices']:
                    n += 1
                    choice_text_out += '\n' + str(n) + ': ' + choice['choice_text']
                event_embed.add_field(name=event['event_text'], value=choice_text_out)
                event_embed.set_footer(text='Answer by inputting the number corresponding to your choice.')
                event_start = await ev.channel.send('Hey ' + message.author.mention + '! An event has appeared!',
                                          embed=event_embed)
                events_active.append(event_id)
                reply = await ev.bot.wait_for_message(timeout=60, author=message.author)
                if not reply:
                    out = discord.Embed(title=':clock10: Sorry, you timed out...', color=0x777777)
                    await ev.channel.send(None, embed=out)
                    await ev.bot.delete_message(event_start)
                    return
                if not reply.content:
                    out = discord.Embed(title='❗ Sorry, I couldn\'t read that...', color=0xDB0000)
                    await ev.channel.send(None, embed=out)
                    await ev.bot.delete_message(event_start)
                    return
                answer = reply.content
                try:
                    answer_number = int(answer)
                    if answer_number < 1:
                        answer_number = 1
                    if answer_number > n:
                        answer_number = n
                except:
                    out = discord.Embed(title='❗ Invalid number input', color=0xDB0000)
                    await ev.channel.send(None, embed=out)
                    events_active.remove(event_id)
                    await ev.bot.delete_message(event_start)
                    return
                answer_index = answer_number - 1
                result = event['choices'][answer_index]
                choice_text = result['choice_text']
                positive = result['positive']
                point_amount = result['points']
                result_text = result['result_text']
                result_embed = discord.Embed(color=0x1abc9c, title='You chose to ' + choice_text.lower())
                await ev.bot.delete_message(event_start)
                if positive:
                    ev.db.add_points(message.guild, message.author, point_amount)
                    result_embed.set_footer(text='You have been awarded ' + str(point_amount) + ' points.')
                else:
                    ev.db.take_points(message.guild, message.author, point_amount)
                    result_embed.set_footer(text='You lost ' + str(point_amount) + ' points.')
                events_active.remove(event_id)
                result_embed.add_field(name='The following happened', value=result_text)
                await ev.channel.send(None, embed=result_embed)
