import aiohttp
import lxml.html as l


async def search_for_scroll(scroll_name):
    scroll_url = f'http://vindictus.gamepedia.com/{scroll_name}_Enchant_Scroll'
    async with aiohttp.ClientSession() as session:
        async with session.get(scroll_url) as data:
            page = await data.text()
    root = l.fromstring(page)
    infobox = root.cssselect('.old-infobox')[0]
    outer_content = root.cssselect('#mw-content-text')[0]

    class Scroll(object):
        name = infobox[0][0][1][0].text
        icon = infobox[0][0][0][0][0][0].attrib['src'].split('?')[0]
        rank_info_row = infobox[0][1][0].text[1:]
        rank = rank_info_row.split(' ')[1]
        type = rank_info_row.split(' ')[2]
        target = infobox[1][0][0].text_content()[2:]
        enchant = infobox[1][2][0][0].text
        stats = []
        for list_item in infobox[1][2][0][1][0]:
            span_list = []
            for span in list_item:
                span_text = span.text_content()
                if span_text.lower() != 'none':
                    span_list.append(span_text)
            stats.append(' '.join(span_list))
        try:
            other = first_method(outer_content)
        except:
            try:
                other = second_method(outer_content)
            except:
                other = None

    return Scroll


def first_method(outer_content):
    class ScrollData(object):
        drop_locations = []
        try:
            for list_item in outer_content[4]:
                drop_locations.append(list_item.text_content())
            success_chance = outer_content[6].text_content().split('\n')[0].split(': ')[1]
            destruction_chance = outer_content[6].text_content().split('\n')[1].split(': ')[1]
        except:
            for list_item in outer_content[5]:
                drop_locations.append(list_item.text_content())
            success_chance = outer_content[7].text_content().split('\n')[0].split(': ')[1]
            destruction_chance = outer_content[7].text_content().split('\n')[1].split(': ')[1]

    return ScrollData


def second_method(outer_content):
    class ScrollData(object):
        drop_locations = []
        droplist = outer_content[2][1][1]
        for list_item in droplist:
            drop_locations.append(list_item.text_content())
        success_chance = None
        destruction_chance = None
        notelist = outer_content[3][1][0]
        for list_item in notelist:
            if list_item.text_content().lower().startswith('success chance'):
                success_chance = list_item.text_content().split(': ')[1]
            elif list_item.text_content().lower().startswith('destruction chance'):
                destruction_chance = list_item.text_content().split(': ')[1]

    return ScrollData
