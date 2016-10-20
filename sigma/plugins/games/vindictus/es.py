import json

with open('scrolls.json', 'r', encoding='utf-8') as scrolls_file:
    scrolls = scrolls_file.read()
    scrolls = json.loads(scrolls)


async def es(cmd, message, args):
    scrl_input = ' '.join(args).lower()
    scrl_input = scrl_input.replace('\'', '').replace(' ', '').replace(' es', '').replace('enchant', '').replace('scroll', '')

    try:
        scrl_name = scrolls[scrl_input]['name']
        scrl_type = scrolls[scrl_input]['type']
        scrl_foreqp = scrolls[scrl_input]['foreqp']
        scrl_rank = scrolls[scrl_input]['rank']
        scrl_stats = ''
        for stats in scrolls[scrl_input]['stats']:
            scrl_stats += '\n - ' + stats
        await cmd.reply('```' +
                                       '\nName: ' + scrl_name + ' Enchant Scroll' +
                                       '\nType: ' + scrl_type +
                                       '\nUsable On: ' + scrl_foreqp +
                                       '\nRank: ' + scrl_rank +
                                       '\nStats: ' + scrl_stats +
                                       '\n```')
    except Exception as e:
        cmd.log.error(e)
        await cmd.reply('Either the scroll was not found, or the blacksmith guy broke it...\nFerghus, this is the last time you touch a scroll!')
