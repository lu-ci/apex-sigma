import praw
import random


async def reddit(cmd, message, args):
    q = ' '.join(args)

    req = praw.Reddit(user_agent='Apex Sigma')

    try:
        posts = req.get_subreddit(str(q)).get_hot(limit=100)
        url_list = []

        for post in posts:
            url_list.append(post.url)

        out_tex = random.choice(url_list)
        await cmd.bot.send_message(message.channel, out_tex)
    except Exception as e:
        cmd.log.error(e)
        await cmd.bot.send_message(message.channel, str(e))
