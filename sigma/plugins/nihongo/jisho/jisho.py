import requests


async def jisho(cmd, message, *args):
    jisho_q = ' '.join(*args)

    request = requests.get('http://jisho.org/api/v1/search/words?keyword=' + jisho_q)

    if request.text.find('503 Service Unavailable') != -1:
        await cmd.bot.send_message(message.channel, 'Jisho responded with 503 Service Unavailable')
        return

    request = request.json()

    # check if response contains data or nothing was found
    if request['data']:
        request = request['data'][0]
    else:
        await cmd.bot.send_message(message.channel, "Sorry, couldn't find anything matching `{}`".format(jisho_q))
        return

    output = '```'
    # if the word doesn't have kanji, print out the kana alone
    try:
        output += "{} 【{}】".format(request['japanese'][0]['word'], request['japanese'][0]['reading'])
    except KeyError:
        output += "{}".format(request['japanese'][0]['reading'])

    # parsing tags
    if request['is_common']:
        output += ' | common word'

    wk_lvls = []

    for tag in request['tags']:
        if tag.find('wanikani') != -1:
            wk_lvls.append(tag[8:])

    if wk_lvls:
        output += ' | Wanikani level {}'.format(', '.join(wk_lvls))

    definitons_len = 1
    if len(request['senses']) > 5:
        definitons_len = 5
    else:
        definitons_len = len(request['senses'])

    for i in range(0, definitons_len):
        output += '\n'
        etc = []
        output += '{}. {}'.format(i + 1, '; '.join(request['senses'][i]['english_definitions']))
        if request['senses'][i]['parts_of_speech']:
            etc.append(', '.join(request['senses'][i]['parts_of_speech']))

        if request['senses'][i]['tags']:
            try:
                etc.append('; '.join(request['senses'][i]['tags']))
            except:
                pass
        if request['senses'][i]['see_also']:
            etc.append('See also {}'.format(', '.join(request['senses'][i]['see_also'])))

        if request['senses'][i]['info']:
            etc.append('; '.join(request['senses'][i]['info']))

        # attaching definition tags
        if etc:
            if etc[0]:
                output += '\n| ' + ', '.join(etc)

        etc += '\n'

    if len(request['senses']) > 5:
        hidden = len(request['senses']) - 5
        if hidden == 1:
            output += '\n- {} definition is hidden' .format(hidden)
        else:
            output += '\n- {} definitions are hidden'.format(hidden)

    other_forms = ''
    if len(request['japanese']) > 1:
        other_forms = ''
        for i in range(1, len(request['japanese'])):
            if 'word' in request['japanese'][i]:
                other_forms += request['japanese'][i]['word'] + '、'
    if other_forms:
        output += '\n\nOther forms ' + other_forms[:-1] + '```'  # account for extra comma
    else:
        output += '```'

    await cmd.bot.send_message(message.channel, output)
