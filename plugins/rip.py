from plugin import Plugin
from config import cmd_rip
import requests
from PIL import Image
from io import BytesIO
class Rip(Plugin):
    is_global = True

    async def on_message(self, message, pfx):
        if message.content.startswith(pfx + cmd_rip):
            result = ''
            mentioned_avatar = ''
            for user in message.mentions:
                result = result + 'The Avatar of ' + user.display_name + " is " + user.avatar_url
                mentioned_avatar = user.avatar_url
            cmd_name = 'Rest In Peace'
            user_avatar = requests.get(mentioned_avatar).content
            base = Image.open('img/rip/base.png')
            tomb = Image.open('img/rip/tombstone.png')
            avatar_img = Image.open(BytesIO(user_avatar))
            base.paste(avatar_img, (52, 160))
            base.paste(tomb, (0, 0), tomb)
            base.save('cache/rip/rip_' + message.author.id + '.png')
            await self.client.send_file(message.channel, 'cache/rip/rip_' + message.author.id + '.png')
