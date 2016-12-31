import discord
import yaml
import random


async def random_event_control(ev, message, args):
    events_enabled = ev.db.get_settings(message.server.id, 'RandomEvents')
    if events_enabled:
        chance = ev.db.get_settings(message.server.id, 'EventChance')
        rolled_number = random.randint(1, 100)
        if rolled_number <= chance:
            with open(ev.resource('events.yml')) as events_file:
                event_data = yaml.load(events_file)
            event = random.choice(event_data['events'])
            event_embed = discord.Embed(color=0x1abc9c, title='💠 An event!')
            choice_text = ''
            n = 0
            for choice in event['choices']:
                n += 1
                choice_text += '\n' + str(n) + ': ' + choice['choice_text']
            event_embed.add_field(name=event['event_text'] + '\nWhat do you do?', value=choice_text)
            event_embed.set_footer(text='Answer by inputting the number corresponding to your choice.')
            await ev.bot.send_message(message.channel, 'Hey ' + message.author.mention + '! An event has appeared!',
                                      embed=event_embed)
