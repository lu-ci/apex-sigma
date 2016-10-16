from plugin import Plugin
from utils import create_logger
import json

with open('scrolls.json', 'r', encoding='utf-8') as scrolls_file:
    scrolls = scrolls_file.read()
    scrolls = json.loads(scrolls)


class VindictusScrollSearch(Plugin):
    is_global = True
    log = create_logger('es')

    async def on_message(self, message, pfx):
        if message.content.startswith(pfx + 'es'):
            await self.client.send_typing(message.channel)
            cmd_name = 'Vindictus Scroll Search'
            try:
                self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                              message.author,
                              message.author.id, message.server.name, message.server.id, message.channel)
            except:
                self.log.info('User %s [%s], used the ' + cmd_name + ' command.',
                              message.author,
                              message.author.id)
            scrl_input = (message.content[len(pfx) + len('es') + 1:]).lower().replace('\'', '').replace(' ', '').replace(' es', '').replace('enchant', '').replace('scroll', '')
            try:
                scrl_name = scrolls[scrl_input]['name']
                scrl_type = scrolls[scrl_input]['type']
                scrl_foreqp = scrolls[scrl_input]['foreqp']
                scrl_rank = scrolls[scrl_input]['rank']
                scrl_stats = ''
                for stats in scrolls[scrl_input]['stats']:
                    scrl_stats += '\n - ' + stats
                await self.client.send_message(message.channel, '```' +
                                               '\nName: ' + scrl_name + ' Enchant Scroll' +
                                               '\nType: ' + scrl_type +
                                               '\nUsable On: ' + scrl_foreqp +
                                               '\nRank: ' + scrl_rank +
                                               '\nStats: ' + scrl_stats +
                                               '\n```')
            except:
                await self.client.send_message(message.channel, 'Either the scroll was not found, or the blacksmith guy broke it...\nFerghus, this is the last time you touch a scroll!')
