import requests
from PIL import Image
from io import BytesIO


async def rip(cmd, message, args):
    result = ''
    mentioned_avatar = ''

    if not message.mentions:
        await cmd.reply(cmd.help())
        return

    for user in message.mentions:
        result = result + 'The Avatar of ' + user.display_name + " is " + user.avatar_url
        mentioned_avatar = user.avatar_url

    user_avatar = requests.get(mentioned_avatar).content
    base = Image.open(cmd.resource('img/base.png'))
    tomb = Image.open(cmd.resource('img/tombstone.png'))
    avatar_img = Image.open(BytesIO(user_avatar))
    base.paste(avatar_img, (52, 160))
    base.paste(tomb, (0, 0), tomb)
    base.save('cache/rip/rip_' + message.author.id + '.png')

    await cmd.reply_file('cache/rip/rip_' + message.author.id + '.png')
