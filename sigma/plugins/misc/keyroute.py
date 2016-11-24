import yaml
import os

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
                    if character in char['name'].lower():
                        char_choice = char
                        break
                if not char_choice:
                    await cmd.bot.send_message(message.channel,
                                               'No Character by the name' + character + ' was found in **' + vn_name + '** was found.')
                    return
                else:
                    char_name = char_choice['name']
                    char_name_j = char_choice['name_j']
                    char_desc = char_choice['description']
                    route = char_choice['route']
                    if route:
                        route_out = ''
                        for choice in route:
                            route_out += '\n - \"' + choice.title() + '\"'
                        route_out = route_out[:-1]
                    else:
                        route_out = 'There Are No Choices On This Route'
                    out = 'Name: **' + char_name + '** | `' + char_name_j + '`'
                    out += '\n```\n' + char_desc + '\n```'
                    out += '\nThe Route Walkthrough is in the text file below. :white_check_mark:'
                    route_out = 'Route Walkthrough for **' + char_name + '** from **' + vn_name + '** :\n```' + route_out + '\n```'
                    with open('cache/key_route_' + message.author.id + '.txt', "w") as text_file:
                        text_file.write(route_out)
                    # await cmd.bot.send_message(message.channel, out)
                    await cmd.bot.send_file(message.channel, 'cache/key_route_' + message.author.id + '.txt', content=out)
                    os.remove('cache/key_route_' + message.author.id + '.txt')
