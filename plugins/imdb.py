from plugin import Plugin
from config import cmd_imdb
from utils import create_logger
import requests


class IMDB(Plugin):
    is_global = True
    log = create_logger(cmd_imdb)

    async def on_message(self, message, pfx):
        if message.content.startswith(pfx + cmd_imdb):
            await self.client.send_typing(message.channel)
            cmd_name = 'Internet Movie DataBase'
            try:
                self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                              message.author,
                              message.author.id, message.server.name, message.server.id, message.channel)
            except:
                self.log.info('User %s [%s], used the ' + cmd_name + ' command.',
                              message.author,
                              message.author.id)
            imdb_imput = message.content[len(pfx) + len(cmd_imdb) + 1:]
            request = requests.get('http://www.omdbapi.com/?t=' + imdb_imput + '&y=&plot=short&r=json').json()
            try:
                title = request['Title']
                rated = request['Rated']
                released = request['Released']
                runtime = request['Runtime']
                genre = request['Genre']
                awards = request['Awards']
                score = request['Metascore']
                rating = request['imdbRating']
                language = request['Language']
                country = request['Country']
                writers = request['Writer']
                directors = request['Director']
                actors = request['Actors']
                plot = request['Plot']
                movie_text = ('```\nTitle: ' + title +
                              '\nReleased: ' + released +
                              '\nRated: ' + rated +
                              '\nRuntime: ' + runtime +
                              '\nGenre: ' + genre +
                              '\nCountry: ' + country +
                              '\nLanguage: ' + language +
                              '\nAwards: ' + awards +
                              '\nWriters: ' + writers +
                              '\nDirectors: ' + directors +
                              '\nActors: ' + actors +
                              '\nMetascore: ' + score +
                              '\nIMDB Rating: ' + rating + '```')
                await self.client.send_message(message.channel, movie_text + '\nPlot:\n```\n' + plot + '\n```')
            except:
                if imdb_imput == '':
                    await self.client.send_message(message.channel, 'You need to specify a movie!')
                else:
                    try:
                        await self.client.send_message(message.channel, 'Error: ' + request['Error'])
                    except:
                        await self.client.send_message(message.channel, 'Something went horribly wrong!')
