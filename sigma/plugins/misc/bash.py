from discord import Embed

cache = []

async def bash(cmd, message, args):
    if len(cache) == 0:
        import lxml.html as l, requests

        page = requests.get('http://bash.org/?random1')
        quotes = l.fromstring(page.content).cssselect('body center table tr td[valign="top"]')[0]
        for index in range(1, len(quotes), 2):
            id = quotes[index - 1][0][0].text
            score = quotes[index - 1][2].text
            quote = quotes[index].text_content()

            quote = {
                'id': id[1:],
                'score': score,
                'quote': quote
            }
            cache.append(quote)

    quote = cache.pop()
    embed = Embed(type='rich', color=0XC08000, title=':scroll: A Bash Quote', description='```xml\n{}```'.format(quote['quote']))
    embed.set_footer(text='ID: {} | Score: {}'.format(quote['id'], quote['score']))

    await cmd.bot.send_message(message.channel, None, embed=embed)
