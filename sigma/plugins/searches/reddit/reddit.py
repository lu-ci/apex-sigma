import praw
import random
from config import RedditClientID, RedditClientSecret


async def reddit(cmd, message, args):
    q = ' '.join(args)

    req = praw.Reddit(user_agent='Apex Sigma', client_id=RedditClientID, client_secret=RedditClientSecret)

    posts = req.subreddit(str(q)).hot(limit=100)
    url_list = []

    for post in posts:
        url_list.append(post.url)

    out_tex = random.choice(url_list)
    await cmd.bot.send_message(message.channel, out_tex)
