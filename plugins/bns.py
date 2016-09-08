from plugin import Plugin
from config import cmd_bns
from config import cmd_bns_att
from config import cmd_bns_def
import requests
from lxml import html
from utils import create_logger

def getSummary(tree):
    summary = {
        'Username' : tree[0][0].text,
        'Nickname' : tree[0][1].text[1: -1],
        'Level' : tree[2][0][1].text[6:],
        'World' : tree[2][0][2].text,
        'Class' : tree[2][0][0].text
    }
    try:
        summary['Faction'] = tree[2][0][3].text
    except IndexError:
        summary['Faction'] = 'None'
    try: #trying to parse guild name, player might not be in any guild
        summary['Guild'] = tree[2][0][4].text
    except IndexError:
        summary['Guild'] = 'None'
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

class BladeAndSoul(Plugin):
    is_global = True
    log = create_logger(cmd_bns)

    async def on_message(self, message, pfx):
        # Blade and Soul API
        if message.content.startswith(pfx + cmd_bns):
            cmd_name = 'Blade and Soul'
            self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel', message.author,
                          message.author.id, message.server.name, message.server.id, message.channel)
            await self.client.send_typing(message.channel)
            query = message.content[len(cmd_bns) + 1 + len(pfx):]
            region = str(query[:query.find(' ')]).lower()
            if not region == 'na' and not region == 'eu':
                error_msg = 'Invalid Region: `' + region + '`\nThe command format is `' + pfx + cmd_bns + ' [region] [Character Name]`\nThe region can be `NA` or `EU` and the character name **CAN** contain spaces.'
                await self.client.send_message(message.channel, error_msg)
            else:
                error_msg = 'Something went wrong, API is unavailable or character does not exist.'
                username = str(query[query.find(' ') + 1:]).lower()
                profile = fetchStats(region, username)
                try:
                    # Summary
                    username = str(profile['Summary']['Username'])
                    nickname = str(profile['Summary']['Nickname'])
                    level = str(profile['Summary']['Level'])
                    world = str(profile['Summary']['World'])
                    ch_class = str(profile['Summary']['Class'])
                    faction = str(profile['Summary']['Faction'])
                    guild = str(profile['Summary']['Guild'])
                    # Attack Stats Basic
                    att_pwr = str(profile['Attack Stats']['Attack Power']['Total'])
                    ev_att_rate = str(profile['Attack Stats']['Evolved Attack Rate']['Total'])
                    pierc = str(profile['Attack Stats']['Piercing']['Total'])
                    pierc_def = str(profile['Attack Stats']['Piercing']['Defense Piercing'])
                    pierc_block = str(profile['Attack Stats']['Piercing']['Block Piercing'])
                    acc = str(profile['Attack Stats']['Accuracy']['Total'])
                    acc_hr = str(profile['Attack Stats']['Accuracy']['Hit Rate'])
                    conc = str(profile['Attack Stats']['Concentration']['Total'])
                    crit_hit = str(profile['Attack Stats']['Critical Hit']['Total'])
                    crit_hit_rate = str(profile['Attack Stats']['Critical Hit']['Critical Rate'])
                    crit_dmg = str(profile['Attack Stats']['Critical Damage']['Total'])
                    crit_dmg_dmg = str(profile['Attack Stats']['Critical Damage']['Increase Damage'])
                    mast = str(profile['Attack Stats']['Mastery']['Total'])
                    add_dmg = str(profile['Attack Stats']['Additional Damage']['Total'])
                    threat = str(profile['Attack Stats']['Threat']['Total'])
                    fire_dmg = str(profile['Attack Stats']['Flame Damage']['Total'])
                    cold_dmg = str(profile['Attack Stats']['Frost Damage']['Total'])
                    # Defense Stats Basic
                    hp = str(profile['Defense Stats']['HP']['Total'])
                    def_tot = str(profile['Defense Stats']['Defense']['Total'])
                    def_dmg_redu = str(profile['Defense Stats']['Defense']['Damage Reduction'])
                    ev_def = str(profile['Defense Stats']['Evolved Defense']['Total'])
                    evasion = str(profile['Defense Stats']['Evasion']['Total'])
                    evasion_rate = str(profile['Defense Stats']['Evasion']['Evasion Rate'])
                    block = str(profile['Defense Stats']['Block']['Total'])
                    block_rate = str(profile['Defense Stats']['Block']['Block Rate'])
                    crit_def = str(profile['Defense Stats']['Critical Defense']['Total'])
                    crit_def_rate = str(profile['Defense Stats']['Critical Defense']['Critical Evasion Rate'])
                    will = str(profile['Defense Stats']['Willpower']['Total'])
                    dmg_redu = str(profile['Defense Stats']['Damage Reduction']['Total'])
                    regen = str(profile['Defense Stats']['Health Regen']['Total'])
                    rec = str(profile['Defense Stats']['Recovery']['Total'])
                    nerf_def = str(profile['Defense Stats']['Debuff Defense']['Total'])
                    # Texts
                    summary_text = (':ticket: Summary:\n```' +
                                    '\nUsername: ' + username +
                                    '\nNickname: ' + nickname +
                                    '\nLevel: ' + level +
                                    '\nWorld: ' + world +
                                    '\nClass: ' + ch_class +
                                    '\nFaction: ' + faction +
                                    '\nGuild: ' + guild +
                                    '\n```')

                    attack_stats_text = (':crossed_swords: Attack Stats: \n```' +
                                         '\nAttack Power: ' + att_pwr +
                                         '\nEvolved Attack Rate: ' + ev_att_rate +
                                         '\nPiercing: ' + pierc + '(DEF:' + pierc_def + '|Block: ' + pierc_block + ')' +
                                         '\nAccuracy: ' + acc + '(' + acc_hr + ')' +
                                         '\nConcentrationr: ' + conc +
                                         '\nCrtitical Hit: ' + crit_hit + '(' + crit_hit_rate + ')' +
                                         '\nCritical Damage: ' + crit_dmg + '(' + crit_dmg_dmg + ')' +
                                         '\nMastery: ' + mast +
                                         '\nAdditional Damage: ' + add_dmg +
                                         '\nThreat: ' + threat +
                                         '\nFlame Damage: ' + fire_dmg +
                                         '\nFrost Damage: ' + cold_dmg +
                                         '\n```')
                    def_stats_text = (':shield: Defense Stats: \n```' +
                                      '\nHP: ' + hp +
                                      '\nDefense: ' + def_tot + '(' + def_dmg_redu + ')' +
                                      '\nEvolved Defense: ' + ev_def +
                                      '\nEvasion: ' + evasion + '(' + evasion_rate + ')' +
                                      '\nBlock: ' + block + '(' + block_rate + ')' +
                                      '\nCritical Defense: ' + crit_def + '(' + crit_def_rate + ')' +
                                      '\nWillpower: ' + will +
                                      '\nDamage Reduction: ' + dmg_redu +
                                      '\nHealth Regen: ' + regen +
                                      '\nRecovery: ' + rec +
                                      '\nDebuff Defense: ' + nerf_def +
                                      '\n```')
                    await self.client.send_message(message.channel, summary_text + attack_stats_text + def_stats_text)
                    # await client.send_message(message.channel, summary_text)
                    # await client.send_message(message.channel, attack_stats_text)
                    # await client.send_message(message.channel, def_stats_text)
                except:
                    await self.client.send_message(message.channel, error_msg)
            #print('CMD [' + cmd_name + '] > ' + initiator_data)
        # Blade and Soul Attack Details API
        elif message.content.startswith(pfx + cmd_bns_att):
            cmd_name = 'Blade and Soul Attack Details'
            self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel', message.author,
                          message.author.id, message.server.name, message.server.id, message.channel)
            await self.client.send_typing(message.channel)
            query = message.content[len(cmd_bns) + 1 + 3 + len(pfx):]
            region = str(query[:query.find(' ')]).lower()
            if not region == 'na' and not region == 'eu':
                error_msg = 'Invalid Region: `' + region + '`\nThe command format is `' + pfx + cmd_bns + ' [region] [Character Name]`\nThe region can be `NA` or `EU` and the character name **CAN** contain spaces.'
                await self.client.send_message(message.channel, error_msg)
            else:
                error_msg = 'Something went wrong, API is unavailable or character does not exist.'
                username = str(query[query.find(' ') + 1:]).lower()
                profile = fetchStats(region, username)
                try:
                    # Summary
                    nickname = str(profile['Summary']['Nickname'])
                    # Attack Stats
                    att_pwr = str(profile['Attack Stats']['Attack Power']['Total'])
                    att_pwr_base = str(profile['Attack Stats']['Attack Power']['Base'])
                    att_pwr_eqp = str(profile['Attack Stats']['Attack Power']['Equipped'])
                    ev_att_rate = str(profile['Attack Stats']['Evolved Attack Rate']['Total'])
                    ev_att_rate_base = str(profile['Attack Stats']['Evolved Attack Rate']['Base'])
                    ev_att_rate_eqp = str(profile['Attack Stats']['Evolved Attack Rate']['Equipped'])
                    pierc = str(profile['Attack Stats']['Piercing']['Total'])
                    pierc_base = str(profile['Attack Stats']['Piercing']['Base'])
                    pierc_eqp = str(profile['Attack Stats']['Piercing']['Equipped'])
                    pierc_def = str(profile['Attack Stats']['Piercing']['Defense Piercing'])
                    pierc_block = str(profile['Attack Stats']['Piercing']['Block Piercing'])
                    acc = str(profile['Attack Stats']['Accuracy']['Total'])
                    acc_base = str(profile['Attack Stats']['Accuracy']['Base'])
                    acc_eqp = str(profile['Attack Stats']['Accuracy']['Equipped'])
                    acc_hr = str(profile['Attack Stats']['Accuracy']['Hit Rate'])
                    conc = str(profile['Attack Stats']['Concentration']['Total'])
                    conc_base = str(profile['Attack Stats']['Concentration']['Base'])
                    conc_eqp = str(profile['Attack Stats']['Concentration']['Equipped'])
                    conc_bsp = str(profile['Attack Stats']['Concentration']['Block Skill Piercing'])
                    conc_csp = str(profile['Attack Stats']['Concentration']['Counter Skill Piercing'])
                    crit_hit = str(profile['Attack Stats']['Critical Hit']['Total'])
                    crit_hit_base = str(profile['Attack Stats']['Critical Hit']['Base'])
                    crit_hit_eqp = str(profile['Attack Stats']['Critical Hit']['Equipped'])
                    crit_hit_rate = str(profile['Attack Stats']['Critical Hit']['Critical Rate'])
                    crit_dmg = str(profile['Attack Stats']['Critical Damage']['Total'])
                    crit_dmg_base = str(profile['Attack Stats']['Critical Damage']['Base'])
                    crit_dmg_eqp = str(profile['Attack Stats']['Critical Damage']['Equipped'])
                    crit_dmg_dmg = str(profile['Attack Stats']['Critical Damage']['Increase Damage'])
                    mast = str(profile['Attack Stats']['Mastery']['Total'])
                    add_dmg = str(profile['Attack Stats']['Additional Damage']['Total'])
                    add_dmg_bonus = str(profile['Attack Stats']['Additional Damage']['Damage Bonus'])
                    threat = str(profile['Attack Stats']['Threat']['Total'])
                    threat_base = str(profile['Attack Stats']['Threat']['Base'])
                    threat_eqp = str(profile['Attack Stats']['Threat']['Equipped'])
                    threat_bonus = str(profile['Attack Stats']['Threat']['Threat Bonus'])
                    fire_dmg = str(profile['Attack Stats']['Flame Damage']['Total'])
                    fire_dmg_base = str(profile['Attack Stats']['Flame Damage']['Base'])
                    fire_dmg_eqp = str(profile['Attack Stats']['Flame Damage']['Equipped'])
                    fire_dmg_rate = str(profile['Attack Stats']['Flame Damage']['Flame Damage Rate'])
                    cold_dmg = str(profile['Attack Stats']['Frost Damage']['Total'])
                    cold_dmg_base = str(profile['Attack Stats']['Frost Damage']['Base'])
                    cold_dmg_eqp = str(profile['Attack Stats']['Frost Damage']['Equipped'])
                    cold_dmg_rate = str(profile['Attack Stats']['Frost Damage']['Frost Damage Rate'])
                    attack_stats_text = (':crossed_swords: Attack Stats for **' + nickname + '**: \n```' +
                                         '\nAttack Power: ' + att_pwr +
                                         '\n(Base: ' + att_pwr_base + '|Equipped: ' + att_pwr_eqp + ')' +
                                         '\nEvolved Attack Rate: ' + ev_att_rate +
                                         '\n(Base: ' + ev_att_rate_base + '|Equipped: ' + ev_att_rate_eqp + ')' +
                                         '\nPiercing: ' + pierc +
                                         '\n(Base: ' + pierc_base + '|Equipped: ' + pierc_eqp + '|DEF: ' + pierc_def + '|Block: ' + pierc_block + ')' +
                                         '\nAccuracy: ' + acc +
                                         '\n(Base: ' + acc_base + '|Equipped: ' + acc_eqp + '|Rate: ' + acc_hr + ')' +
                                         '\nConcentrationr: ' + conc +
                                         '\n(Base: ' + conc_base + '|Equipped: ' + conc_eqp + '|BSP: ' + conc_bsp + '|CSP: ' + conc_csp + ')' +
                                         '\nCrtitical Hit: ' + crit_hit +
                                         '\n(Base: ' + crit_hit_base + '|Equipped: ' + crit_hit_eqp + '|Rate:' + crit_hit_rate + ')' +
                                         '\nCritical Damage: ' + crit_dmg +
                                         '\n(Base: ' + crit_dmg_base + '|Equipped: ' + crit_dmg_eqp + '|DMG: ' + crit_dmg_dmg + ')' +
                                         '\nMastery: ' + mast +
                                         '\nAdditional Damage: ' + add_dmg +
                                         '\n(DMG Bonus: ' + add_dmg_bonus + ')' +
                                         '\nThreat: ' + threat +
                                         '\n(Base: ' + threat_base + '|Equipped: ' + threat_eqp + '|Bonus:' + threat_bonus + ')' +
                                         '\nFlame Damage: ' + fire_dmg +
                                         '\n(Base: ' + fire_dmg_base + '|Equipped: ' + fire_dmg_eqp + '|Rate: ' + fire_dmg_rate + ')' +
                                         '\nFrost Damage: ' + cold_dmg +
                                         '\n(Base: ' + cold_dmg_base + '|Equipped: ' + cold_dmg_eqp + '|Rate: ' + cold_dmg_rate + ')' +
                                         '\n```')
                    await self.client.send_message(message.channel, attack_stats_text)
                except:
                    await self.client.send_message(message.channel, error_msg)
            #print('CMD [' + cmd_name + '] > ' + initiator_data)
        # Blade and Soul Defense Details API
        elif message.content.startswith(pfx + cmd_bns_def):
            cmd_name = 'Blade and Soul Defense Details'
            self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel', message.author,
                          message.author.id, message.server.name, message.server.id, message.channel)
            await self.client.send_typing(message.channel)
            query = message.content[len(cmd_bns) + 1 + 3 + len(pfx):]
            region = str(query[:query.find(' ')]).lower()
            if not region == 'na' and not region == 'eu':
                error_msg = 'Invalid Region: `' + region + '`\nThe command format is `' + pfx + cmd_bns + ' [region] [Character Name]`\nThe region can be `NA` or `EU` and the character name **CAN** contain spaces.'
                await self.client.send_message(message.channel, error_msg)
            else:
                error_msg = 'Something went wrong, API is unavailable or character does not exist.'
                username = str(query[query.find(' ') + 1:]).lower()
                profile = fetchStats(region, username)
                try:
                    # Summary
                    nickname = str(profile['Summary']['Nickname'])
                    # Defense Stats
                    hp = str(profile['Defense Stats']['HP']['Total'])
                    hp_base = str(profile['Defense Stats']['HP']['Base'])
                    hp_eqp = str(profile['Defense Stats']['HP']['Equipped'])
                    def_tot = str(profile['Defense Stats']['Defense']['Total'])
                    def_base = str(profile['Defense Stats']['Defense']['Base'])
                    def_eqp = str(profile['Defense Stats']['Defense']['Equipped'])
                    def_dmg_redu = str(profile['Defense Stats']['Defense']['Damage Reduction'])
                    def_aoe = str(profile['Defense Stats']['Defense']['AoE Defense'])
                    def_aoe_redu = str(profile['Defense Stats']['Defense']['AoE Defense Reduction'])
                    ev_def = str(profile['Defense Stats']['Evolved Defense']['Total'])
                    ev_def_base = str(profile['Defense Stats']['Evolved Defense']['Base'])
                    ev_def_eqp = str(profile['Defense Stats']['Evolved Defense']['Equipped'])
                    ev_def_rate = str(profile['Defense Stats']['Evolved Defense']['Evolved Defense Rate'])
                    ev_def_aoe = str(profile['Defense Stats']['Evolved Defense']['AoE Defense'])
                    ev_def_aoe_dmg_redu = str(profile['Defense Stats']['Evolved Defense']['AoE Defense Reduction'])
                    evasion = str(profile['Defense Stats']['Evasion']['Total'])
                    evasion_base = str(profile['Defense Stats']['Evasion']['Base'])
                    evastion_eqp = str(profile['Defense Stats']['Evasion']['Equipped'])
                    evasion_rate = str(profile['Defense Stats']['Evasion']['Evasion Rate'])
                    evasion_ctr = str(profile['Defense Stats']['Evasion']['Counter Bonus'])
                    block = str(profile['Defense Stats']['Block']['Total'])
                    block_base = str(profile['Defense Stats']['Block']['Base'])
                    block_eqp = str(profile['Defense Stats']['Block']['Equipped'])
                    block_rate = str(profile['Defense Stats']['Block']['Block Rate'])
                    block_bonus = str(profile['Defense Stats']['Block']['Block Bonus'])
                    block_dmg_redu = str(profile['Defense Stats']['Block']['Damage Reduction'])
                    crit_def = str(profile['Defense Stats']['Critical Defense']['Total'])
                    crit_def_rate = str(profile['Defense Stats']['Critical Defense']['Critical Evasion Rate'])
                    crit_def_dmg_redu = str(profile['Defense Stats']['Critical Defense']['Damage Reduction'])
                    will = str(profile['Defense Stats']['Willpower']['Total'])
                    dmg_redu = str(profile['Defense Stats']['Damage Reduction']['Total'])
                    dmg_redu_dmg_redu = str(profile['Defense Stats']['Damage Reduction']['Damage Reduction'])
                    regen = str(profile['Defense Stats']['Health Regen']['Total'])
                    regen_in = str(profile['Defense Stats']['Health Regen']['In Combat'])
                    regen_out = str(profile['Defense Stats']['Health Regen']['Out of Combat'])
                    rec = str(profile['Defense Stats']['Recovery']['Total'])
                    rec_pt = str(profile['Defense Stats']['Recovery']['Recovery'])
                    rec_add = str(profile['Defense Stats']['Recovery']['Additional Recovery'])
                    rec_rate = str(profile['Defense Stats']['Recovery']['Recovery Rate'])
                    nerf_def = str(profile['Defense Stats']['Debuff Defense']['Total'])
                    nerf_def_rate = str(profile['Defense Stats']['Debuff Defense']['Debuff Defense Rate'])
                    def_stats_text = (':shield: Defense Stats for **' + nickname + '**: \n```' +
                                      '\nHP: ' + hp +
                                      '\n(Base: ' + hp_base + '|Equipped: ' + hp_eqp + ')' +
                                      '\nDefense: ' + def_tot +
                                      '\n(Base: ' + def_base + '|Equipped: ' + def_eqp + '|DMG Reduction: ' + def_dmg_redu + '|AoE DEF: ' + def_aoe + '|AoE DMG Reduction: ' + def_aoe_redu + ')' +
                                      '\nEvolved Defense: ' + ev_def +
                                      '\n(Base: ' + ev_def_base + '|Equipped: ' + ev_def_eqp + '|Defense Rate: ' + ev_def_rate + '|AoE Defense: ' + ev_def_aoe + '|AoE DMG Reduction: ' + ev_def_aoe_dmg_redu + ')' +
                                      '\nEvasion: ' + evasion +
                                      '\n(Base: ' + evasion_base + '|Equipped: ' + evastion_eqp + '|Rate: ' + evasion_rate + '|Counter Bonus: ' + evasion_ctr + ')' +
                                      '\nBlock: ' + block +
                                      '\n(Base: ' + block_base + '|Equipped: ' + block_eqp + '|DMG Redu: ' + block_dmg_redu + '|Bonus: ' + block_bonus + '|Rate: ' + block_rate + ')' +
                                      '\nCritical Defense: ' + crit_def +
                                      '\n(Rate: ' + crit_def_rate + '|DMG Reduction: ' + crit_def_dmg_redu + ')' +
                                      '\nWillpower: ' + will +
                                      '\nDamage Reduction: ' + dmg_redu +
                                      '\n(DMG Redu: ' + dmg_redu_dmg_redu + ')' +
                                      '\nHealth Regen: ' + regen +
                                      '\n(Out of Combat: ' + regen_out + '|In Combat: ' + regen_in + ')' +
                                      '\nRecovery: ' + rec +
                                      '\n(Recovery: ' + rec_pt + '|Additional: ' + rec_add + '|Rate: ' + rec_rate + ')' +
                                      '\nDebuff Defense: ' + nerf_def +
                                      '\n(Rate: ' + nerf_def_rate + ')' +
                                      '\n```')
                    await self.client.send_message(message.channel, def_stats_text)
                except:
                    await self.client.send_message(message.channel, error_msg)
            #print('CMD [' + cmd_name + '] > ' + initiator_data)


