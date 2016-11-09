from .bns import fetchStats


# Blade and Soul Defense Details API
async def bnsdef(cmd, message, args):
    query = message.content[len('bnsdef') + 1 + 3 + len(cmd.prefix):]
    region = str(query[:query.find(' ')]).lower()

    if not region == 'na' and not region == 'eu':
        error_msg = 'Invalid Region: `' + region + '`\nThe command format is `' + cmd.prefix + 'bnsdef [region] [Character Name]`\nThe region can be `NA` or `EU` and the character name **CAN** contain spaces.'
        await cmd.bot.send_message(message.channel, error_msg)
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
            await cmd.bot.send_message(message.channel, def_stats_text)
        except:
            await cmd.bot.send_message(message.channel, error_msg)
