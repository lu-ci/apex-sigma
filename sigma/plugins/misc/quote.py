import requests


async def quote(cmd, message, args):
    try:
        resource = 'http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en'
        data = requests.get(resource).json()
        text = data['quoteText']
        while text.endswith(' '):
            text = text[:-1]
        try:
            author = data['quoteAuthor']
        except:
            author = 'Unknown'
        if author == '':
            author = 'Unknown'
        await cmd.reply('```yaml\n\"' + text + '\"\n    - by ' + author + '\n```')
    except Exception as e:
        cmd.log.error(e)
        await cmd.reply(str(e))
