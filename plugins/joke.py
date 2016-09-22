from plugin import Plugin
from config import cmd_joke
import random
import requests
from utils import create_logger
import json
import asyncio


class Joke(Plugin):
    is_global = True
    log = create_logger(cmd_joke)

    async def on_message(self, message, pfx):
        if message.content.startswith(pfx + cmd_joke):
            cmd_name = 'Joke'
            try:
                self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                              message.author,
                              message.author.id, message.server.name, message.server.id, message.channel)
            except:
                self.log.info('User %s [%s], used the ' + cmd_name + ' command.',
                              message.author,
                              message.author.id)
            number_list = [0, 1, 2]
            joke_no = random.choice(number_list)
            await self.client.send_typing(message.channel)
            if joke_no == 0:
                joke_type = 'Chuck Noris Joke'
                joke_url = 'https://api.chucknorris.io/jokes/random'
                joke_json = requests.get(joke_url).json()
                joke = joke_json['value']
            elif joke_no == 1:
                joke_type = 'Ron Swanson Quote'
                joke_url = 'http://ron-swanson-quotes.herokuapp.com/v2/quotes'
                joke_json = requests.get(joke_url).json()
                joke = joke_json[0]
            elif joke_no == 2:
                comic_no = str(random.randint(1, 1724))
                joke_type = 'xkcd Story'
                joke_url = 'http://xkcd.com/' + comic_no + '/info.0.json'
                joke_json = requests.get(joke_url).json()
                joke = ('#' + comic_no + ' - ' + joke_json['title'] + '\n\n' + joke_json['transcript'])
            else:
                joke_type = 'Normal Joke'
                joke_url = 'http://tambal.azurewebsites.net/joke/random'
                joke_json = requests.get(joke_url).json()
                joke = joke_json['joke']
            await self.client.send_message(message.channel, 'Here, have a ' + joke_type + '!\n```' + joke + '\n```')
            #print('CMD [' + cmd_name + '] > ' + initiator_data)
        elif message.content.startswith(pfx + 'pun'):
            cmd_name = 'Pun'
            await self.client.send_typing(message.channel)
            try:
                self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                              message.author,
                              message.author.id, message.server.name, message.server.id, message.channel)
            except:
                self.log.info('User %s [%s], used the ' + cmd_name + ' command.',
                              message.author,
                              message.author.id)
            try:
                pun_url = 'http://www.punoftheday.com/cgi-bin/arandompun.pl'
                pun_req = requests.get(pun_url).content
                pun_text = (str(pun_req)[len('b\'document.write(\\\'&quot;'):-len('&quot;<br />\\\')\ndocument.write(\\\'<i>&copy; 1996-2016 <a href="http://www.punoftheday.com">Pun of the Day.com</a></i><br />\\\')\\n\'') - 1]).replace('&rsquo;','\'')
                await self.client.send_message(message.channel, 'You\'ve asked for it...\n```' + pun_text + '\n```')
            except:
                await self.client.send_message(message.channel, 'Um, so... we have a bug in the code...\nI failed to retrieve a pun...')
        elif message.content.startswith(pfx + 'dadjoke'):
            with open('storage/dadjokes.json', 'r', encoding='utf-8') as dadjokes_file:
                await self.client.send_typing(message.channel)
                cmd_name = 'Joke'
                try:
                    self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                                  message.author,
                                  message.author.id, message.server.name, message.server.id, message.channel)
                except:
                    self.log.info('User %s [%s], used the ' + cmd_name + ' command.',
                                  message.author,
                                  message.author.id)
                jokes = dadjokes_file.read()
                jokes = json.loads(jokes)
                print(len(jokes['JOKES']))
                joke_list = jokes['JOKES']
                end_joke_choice = random.choice(joke_list)
                end_joke = (end_joke_choice['setup'])
                punchline = ('\n\n' + end_joke_choice['punchline'])
                joke_msg = await self.client.send_message(message.channel,'I can\'t believe I\'m doing this...\n```' + end_joke + '```')
                await asyncio.sleep(3)
                await self.client.edit_message(joke_msg,'I can\'t believe I\'m doing this...\n```' + end_joke + punchline + '```')