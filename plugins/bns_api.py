import requests
from lxml import html

def getSummary(tree):
    summary = {
        'Username' : tree[0][0].text,
        'Nickname' : tree[0][1].text[1: -1],
        'Level' : tree[2][0][1].text,
        'World' : tree[2][0][2].text,
        'Class' : tree[2][0][0].text,
        'Faction' : tree[2][0][3].text
    }
    try: #trying to parse guild name, player might not be in any guild
        summary['Guild'] = tree[2][0][4].text
    except IndexError:
        pass
    return summary

def getStats(tree):
    out = {}
    #Collecting attack stats
    for i in range(0, len(tree), 2):
        title = tree[i][1].text
        total = tree[i][2].text

        #collecting all stats in a single array
        #in key, value, key, value formatting
        substats = ['Total', total]
        try:
            for elem in tree[i + 1][0]:
                for subel in elem:
                    if subel.tag == 'span':
                        substats.append(subel.text)
        except IndexError: pass

        #splitting the stats in json
        stats = {}
        for index in range(0, len(substats), 2):
            stats[substats[index]] = ''
        for index in range(1, len(substats), 2):
            stats[substats[index - 1]] = substats[index]
        stats = {title : stats} #wrapping them
        out[title] = stats[title]
    return out

def getEquipment(tree):
    weapon_name = ''
    weapon_quality = ''
    weapon_gems = []

    try: weapon_name = tree[2][1][0].text
    except: pass

    try: weapon_quality = tree[2][0][3][2].text
    except: pass

    try:
        for element in tree[2][3]:
            weapon_gems.append(element[0].attrib['alt'])
    except: pass

    accessories = []
    for i in range(4, 24, 2):
        if tree[i][1][0].attrib['class'] != 'empty':
            accessories.append(tree[i][1][0].text)
        else: accessories.append('')

    equipment = {
        'Weapon' : {
            'Name' : weapon_name,
            'Quality' : weapon_quality,
            'Gems' : weapon_gems
        },
        'Accessories' : {
            'Necklace' : accessories[0],
            'Earring' : accessories[1],
            'Ring' : accessories[2],
            'Bracelet' : accessories[3],
            'Belt' : accessories[4],
            'Soul' : accessories[5],
            'Clothes' : accessories[6],
            'Head Adornment' : accessories[7],
            'Face Adornment' : accessories[8],
            'Adornment' : accessories[9]
        }
    }
    return equipment

def getSoulShieldStats(tree):
    output = {}
    for element in tree:
        name = element[0].text
        total = element[1][0].text
        fused = element[1][1].text
        set = element[1][2].text
        base = str(int(total) - (int(fused) + int(set)))
        substats = {
            'Total' : total,
            'Base' : base,
            'Fused' : fused,
            'Set' : set
        }
        output[name] = substats
    return output

def getSoulShieldEffect(tree):
    name = tree[3].text
    string = html.tostring(tree[4]).decode('utf-8')
    string = string[21:].strip()
    effects = []
    while True:
        br = string.find('<br>')
        effects.append(string[:br])
        string = string[br + 4:].strip()
        if string == '</p>': break
    return {
        'Passive' : {
            'Name' : name,
            'Effects' : effects
        }
    }

def fetchStats(region, nickname):
    query = 'http://' + region + '-bns.ncsoft.com/ingame/bs/character/profile?c=' + nickname.replace(' ', '%20')
    page = requests.get(query)
    tree = html.fromstring(page.content)

    try:
        summary = tree.xpath('//header[@id="header"]/dl')[0]
        attackStats = tree.xpath('//div[@class="statArea"]/div/div[@class="attack"]/dl[@class="stat-define"]')[0]
        defenseStats = tree.xpath('//div[@class="statArea"]/div/div[@class="defense"]/dl[@class="stat-define"]')[0]
        equip = tree.xpath('//div[@class="wrapItem"]')[0]
        soulShield = tree.xpath('//div[@id="charmEffect"]/div/table')[0]

        output = {}
        output['Summary'] = getSummary(summary)
        output['Attack Stats'] = getStats(attackStats)
        output['Defense Stats'] = getStats(defenseStats)
        output['Equipment'] = getEquipment(equip)
        output['Soul Shield'] = getSoulShieldStats(soulShield)
        try:
            soulShieldEffect = tree.xpath('//div[@id="charmEffect"]/div')[0]
            output['Soul Shield'] = getSoulShieldEffect(soulShieldEffect)
        except:
            pass
        return output
    except:
        return {
            'Error' : 'Something went wrong'
        }