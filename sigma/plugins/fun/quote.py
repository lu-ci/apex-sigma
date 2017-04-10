import aiohttp
import discord


async def quote(cmd, message, args):
    resource = 'http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en'
    data = None
    tries = 0
    while not data and tries < 5:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(resource) as data:
                    data = await data.json()
        except:
            tries += 1
    if data:
        text = data['quoteText']
        while text.endswith(' '):
            text = text[:-1]
        try:
            author = data['quoteAuthor']
        except:
            author = 'Unknown'
        if author == '':
            author = 'Unknown'
        quote_text = '```yaml\n\"' + text + '\"\n    - by ' + author + '\n```'
        embed = discord.Embed(color=0x1abc9c)
        embed.add_field(name='📑 Wise words...', value=quote_text)
        await message.channel.send(None, embed=embed)
