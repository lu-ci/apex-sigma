import requests


async def imdb(cmd, message, args):
    imdb_imput = ' '.join(args)

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
        await cmd.bot.send_message(message.channel, movie_text + '\nPlot:\n```\n' + plot + '\n```')
    except:
        if imdb_imput == '':
            await cmd.bot.send_message(message.channel, 'You need to specify a movie!')
        else:
            try:
                await cmd.bot.send_message(message.channel, 'Error: ' + request['Error'])
            except Exception as e:
                cmd.log.error(e)
                await cmd.bot.send_message(message.channel, 'Something went horribly wrong!')
