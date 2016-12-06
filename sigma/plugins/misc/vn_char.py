import lxml.html as l
import requests


def key_char_parse(char_id):
    url = 'https://vndb.org/c' + str(char_id)
    page = requests.get(url)
    root = l.fromstring(page.text)

    name = root.cssselect('.mainbox h1')[0].text
    kanji_name = root.cssselect('.mainbox h2.alttitle')[0].text
    img = 'https:' + root.cssselect('.mainbox .charimg img')[0].attrib['src']
    gender = root.cssselect('.chardetails table thead tr td abbr')[0].attrib['title']
    try:
        bloodtype = root.cssselect('.chardetails table thead tr td span')[0].text
    except IndexError:
        bloodtype = None

    table = root.cssselect('.chardetails table')[0]
    for row in table:
        if row.tag == 'tr':
            if len(row) == 2:
                try:
                    key = row[0][0].text
                except IndexError:
                    key = row[0].text

                value = None
                try:
                    if row[1][0].tag == 'a':
                        value = row[1][0].text
                    else:
                        value = []
                        for span in row[1]:
                            if 'charspoil_1' in span.classes:
                                tag = 'minor spoiler'
                            elif 'charspoil_2' in span.classes:
                                tag = 'spoiler'
                            elif 'sexual' in span.classes:
                                tag = 'sexual trait'
                            else:
                                tag = None

                            value.append({'value': span[1].text, 'tag': tag})
                except IndexError:
                    value = row[1].text

                if key == 'Visual novels':
                    value = []
                    for span in row[1]:
                        if span.tag == 'span':
                            value.append(span.text + span[0].text)
    desc = root.cssselect('.chardetails table td.chardesc')[0][1].text

    character = {
        'URL': url,
        'Name': name,
        'Name_J': kanji_name,
        'Image': img,
        'Gender': gender,
        'Blood_Type': bloodtype,
        'Description': desc
    }
    return character
