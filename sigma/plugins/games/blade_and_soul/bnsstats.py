from .bns import fetchStats


# Blade and Soul API
async def bnsstats(cmd, message, args):
    query = ' '.join(args)
    region = str(query[:query.find(' ')]).lower()

    if not region == 'na' and not region == 'eu':
        error_msg = 'Invalid Region: `' + region + '`\nThe command format is `' + cmd.prefix + 'bnsstats [region] [Character Name]`\nThe region can be `NA` or `EU` and the character name **CAN** contain spaces.'
        await cmd.bot.send_message(message.channel, error_msg)
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
            await cmd.bot.send_message(message.channel, summary_text + attack_stats_text + def_stats_text)
            # await client.send_message(message.channel, summary_text)
            # await client.send_message(message.channel, attack_stats_text)
            # await client.send_message(message.channel, def_stats_text)
        except:
            await cmd.bot.send_message(message.channel, error_msg)
