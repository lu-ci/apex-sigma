from plugin import Plugin
from config import cmd_sonarr
from config import SonarrKey as apikey
from hurry.filesize import size
import requests
from utils import create_logger


class Sonarr(Plugin):
    is_global = True
    log = create_logger(cmd_sonarr)

    async def on_message(self, message, pfx):
        if message.content.startswith(pfx + cmd_sonarr + ' '):
            await self.client.send_typing(message.channel)
            cmd_name = 'Sonarr'
            self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                          message.author,
                          message.author.id, message.server.name, message.server.id, message.channel)
            snr_input = (str(message.content[len(cmd_sonarr) + 1 + len(pfx):]))
            snr_url = 'http://localhost:38082/api/' + snr_input + '?apikey=' + apikey
            snr_data = requests.get(snr_url).json()
            out_text = '```\n'
            if snr_input == 'series':
                for entry in snr_data:
                    out_text += '\n' + entry['title'] + '\nProgress: ' + str(
                        entry['episodeFileCount'] / entry['episodeCount'] * 100) + '%'
                out_text += '\n```'
            elif snr_input == 'calendar':
                for entry in snr_data:
                    out_text += '\nSeries: \"' + entry['series']['title'] + '\"\nEpisode Number: ' + str(
                        entry['episodeNumber']) + '\nEpisode Title:\"' + entry['title'] + '\"\nAir Date: ' + entry[
                                    'airDate'] + '\n'
                out_text += '\n```'
            elif snr_input == 'diskspace':
                for entry in snr_data:
                    out_text += '\nName: ' + entry['label'] + '\nPath: ' + entry['path'] + '\nSpace: ' + str(size(entry['freeSpace'])) + '(' + str(size(entry['totalSpace'])) + ')\n'
                out_text += '\n```'
            else:
                out_text = 'Invalid Parameter :bug:'
            if len(out_text) > 1950:
                out_text = out_text[:1950] + '...\n```\nThe Rest was too long...'
            await self.client.send_message(message.channel, out_text)
