import hashlib


async def gravatar(cmd, message, args):
    if args:
        email = args[0]
        email = email.encode('utf-8')
        gravatar_url = "https://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
        await cmd.reply(gravatar_url)
    else:
        await cmd.reply(cmd.help())
        return
