from plugin import Plugin
from config import cmd_rip
import requests
from PIL import Image
from io import BytesIO
from utils import create_logger

class Rip(Plugin):
    is_global = True
    log = create_logger(cmd_rip)

    async def on_message(self, message, pfx):
        if message.content.startswith(pfx + cmd_rip):
            result = ''
            mentioned_avatar = ''
            for user in message.mentions:
                result = result + 'The Avatar of ' + user.display_name + " is " + user.avatar_url
                mentioned_avatar = user.avatar_url
            cmd_name = 'Rest In Peace'
            try:
                self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                              message.author,
                              message.author.id, message.server.name, message.server.id, message.channel)
            except:
                self.log.info('User %s [%s], used the ' + cmd_name + ' command.',
                              message.author,
                              message.author.id)
            user_avatar = requests.get(mentioned_avatar).content
            base = Image.open('img/rip/base.png')
            tomb = Image.open('img/rip/tombstone.png')
            avatar_img = Image.open(BytesIO(user_avatar))
            base.paste(avatar_img, (52, 160))
            base.paste(tomb, (0, 0), tomb)
            base.save('cache/rip/rip_' + message.author.id + '.png')
            await self.client.send_file(message.channel, 'cache/rip/rip_' + message.author.id + '.png')
