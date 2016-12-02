import requests


async def pun(cmd, message, args):
    try:
        cmd.db.add_stats('CancerCount')

        pun_url = 'http://www.punoftheday.com/cgi-bin/arandompun.pl'
        pun_req = requests.get(pun_url).content
        pun_text = (str(pun_req)[len('b\'document.write(\\\'&quot;'):-len('&quot;<br />\\\')\ndocument.write(\\\'<i>&copy; 1996-2016 <a href="http://www.punoftheday.com">Pun of the Day.com</a></i><br />\\\')\\n\'') - 1]).replace('&rsquo;', '\'')
        await cmd.bot.send_message(message.channel, 'You\'ve asked for it...\n```' + pun_text + '\n```')
    except Exception as e:
        cmd.log.error(e)
        await cmd.bot.send_message(message.channel, 'Um, so... we have a bug in the code...\nI failed to retrieve a pun...')
