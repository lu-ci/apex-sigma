from discord import Embed
import lxml.html as l
import aiohttp

cache = []

async def bash(cmd, message, args):
    if len(cache) == 0:
        async with aiohttp.ClientSession() as session:
            async with session.get('http://bash.org/?random1') as page:
                page = await page.text()
                quotes = l.fromstring(page).cssselect('body center table tr td[valign="top"]')[0]
        for index in range(1, len(quotes), 2):
            qid = quotes[index - 1][0][0].text
            score = quotes[index - 1][2].text
            quote = quotes[index].text_content()

            quote = {
                'id': qid[1:],
                'score': score,
                'quote': quote
            }
            cache.append(quote)

    quote = cache.pop()
    text = quote['quote']
    embed = Embed(type='rich', color=0XC08000, title=':scroll: A Bash Quote', description=f'```xml\n{text}\n```')
    embed.set_footer(text='ID: {} | Score: {}'.format(quote['id'], quote['score']))

    await message.channel.send(None, embed=embed)
