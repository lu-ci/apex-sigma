import requests
import discord


async def imdb(cmd, message, args):
    if not args:
        return

    imdb_imput = ' '.join(args)
    request = requests.get('http://www.omdbapi.com/?t=' + imdb_imput + '&y=&plot=short&r=json').json()
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
    embed = discord.Embed(color=0x1abc9c)
    embed.add_field(name='🎥 Movie Details', value=movie_text)
    embed.add_field(name='📑 Plot', value='```\n' + plot + '\n```')
    await cmd.bot.send_message(message.channel, None, embed=embed)
