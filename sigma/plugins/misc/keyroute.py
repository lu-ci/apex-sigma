import yaml
import os
from humanfriendly.tables import format_pretty_table as boop


async def keyroute(cmd, message, args):
    if not args:
        await cmd.bot.send_message(message.channel, cmd.help())
        return
    else:
        if len(args) < 2:
            await cmd.bot.send_message(message.channel, cmd.help())
            return
        else:
            visual_novel = ' '.join(args[:-1]).lower()
            character = args[-1].lower()
            vn_choice = None
            with open(cmd.resource('routes.yml'), encoding='utf-8') as route_file:
                data = yaml.load(route_file)
                vns = data['vns']
            for vn in vns:
                try:
                    excluders = vn['excluders']
                except:
                    excluders = ['this is here cause an empty list screws it up']
                triggers = vn['triggers']
                for trigger in triggers:
                    for excluder in excluders:
                        if trigger in visual_novel.lower() and excluder not in visual_novel.lower():
                            vn_choice = vn
                            break
            if not vn_choice:
                await cmd.bot.send_message(message.channel,
                                           'No Visual Novel by the name **' + visual_novel + '** was found.')
                return
            else:
                vn_name = vn_choice['name']
                char_choice = None
                for char in vn_choice['characters']:
                    if char['name_j']:
                        if character in char['name'].lower() or character in char['name_j'].lower():
                            char_choice = char
                            break
                    else:
                        if character in char['name'].lower():
                            char_choice = char
                            break
                if not char_choice:
                    await cmd.bot.send_message(message.channel,
                                               'No Route by the name' + character + ' was found in **' + vn_name + '**.')
                    return
                else:
                    char_name = char_choice['name']
                    char_name_j = char_choice['name_j']
                    route = char_choice['route']
                    details = char_choice['details']
                    description = char_choice['description']
                    if route:
                        route_file = cmd.resource('routes/' + route + '.txt')
                        send_route = True
                    else:
                        send_route = False
                    out = 'Name: **' + char_name + '**'
                    if char_name_j:
                        out += ' | **' + char_name_j + '**'
                    if details:
                        detail_list = []
                        for detail in sorted(details):
                            detail_list.append([detail.title().replace('_Ex', '_(Sexual)'), details[detail].title()])
                        details_out = boop(detail_list).replace('_', ' ')
                        out += '\n```\n' + details_out + '\n```'
                    if description:
                        out += '\n```\n' + description + '\n```'
                    if send_route:
                        out += '\nThe Route Walkthrough is in the text file below.'
                        await cmd.bot.send_file(message.channel, route_file, content=out)
                    else:
                        out += '\nThis Route has no choices or the choices are not important.'
                        await cmd.bot.send_message(message.channel, out)
