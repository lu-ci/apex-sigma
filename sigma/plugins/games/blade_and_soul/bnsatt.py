from .bns import fetchStats


# Blade and Soul Attack Details API
async def bnsatt(cmd, message, attr):
    query = message.content[len('bnsatt') + 1 + 3 + len(cmd.prefix):]
    region = str(query[:query.find(' ')]).lower()

    if not region == 'na' and not region == 'eu':
        error_msg = 'Invalid Region: `' + region + '`\nThe command format is `' + cmd.prefix + 'bnsatt [region] [Character Name]`\nThe region can be `NA` or `EU` and the character name **CAN** contain spaces.'
        await cmd.bot.send_message(message.channel, error_msg)
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
            await cmd.bot.send_message(message.channel, attack_stats_text)
        except:
            await cmd.bot.send_message(message.channel, error_msg)
