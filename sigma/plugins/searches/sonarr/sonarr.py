import requests
from hurry.filesize import size

from config import SonarrKey as apikey


async def sonarr(cmd, message, args):
    snr_input = ' '.join(args)

    snr_url = 'http://localhost:38082/api/' + snr_input + '?apikey=' + apikey
    snr_data = requests.get(snr_url).json()
    out_text = ''

    if snr_input == 'series':
        for entry in snr_data:
            out_text += '\n' + entry['title'] + '\nDownload Progress: ' + str(round(
                entry['episodeFileCount'] / entry[
                    'episodeCount'] * 100)) + '%\n[------------------------------]'

        with open("Output.txt", "w") as text_file:
            text_file.write(out_text)
    elif snr_input == 'calendar':
        out_text += '```\n'

        for entry in snr_data:
            out_text += '\nSeries: \"' + entry['series']['title'] + '\"\nEpisode Number: ' + str(
                entry['episodeNumber']) + '\nEpisode Title:\"' + entry['title'] + '\"\nAir Date: ' + entry[
                            'airDate'] + '\n'

        out_text += '\n```'
    elif snr_input == 'diskspace':
        out_text += '```\n'

        for entry in snr_data:
            out_text += '\nName: ' + entry['label'] + '\nPath: ' + entry['path'] + '\nSpace: ' + str(
                size(entry['freeSpace'])) + '(' + str(size(entry['totalSpace'])) + ')\n'

        out_text += '\n```'
    else:
        out_text = 'Invalid Parameter :bug:'

    if snr_input == 'series':
        await cmd.bot.send_file(message.channel, 'Output.txt')
    else:
        await cmd.bot.send_message(message.channel, out_text)
