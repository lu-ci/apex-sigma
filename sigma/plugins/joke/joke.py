import random
import requests

async def joke(cmd, message, args):
    number_list = [0, 1, 2]

    joke_no = random.choice(number_list)

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

    await cmd.bot.send_message(message.channel, 'Here, have a ' + joke_type + '!\n```' + joke + '\n```')
