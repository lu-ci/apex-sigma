import random
import asyncio
import arrow
import discord
from config import SlotWinChannelID

slot_back_data = {}


async def spin_slots(cmd, message, bet_amt, symbols, min_spins=4, max_spins=8, spin_cycle_timeout=1):
    # Cooldown Check
    not_on_cd = True
    current_time = arrow.utcnow().timestamp
    if message.author.id in slot_back_data:
        cd_timestamp = slot_back_data[message.author.id]
        if cd_timestamp + 60 > current_time:
            not_on_cd = False
        else:
            not_on_cd = True
    # Spinnage
    if not_on_cd:
        player_points = cmd.db.get_points(message.author)
        if player_points['Current'] < bet_amt:
            embed = discord.Embed(color=0xDB0000, title='❗ Not Enough Points')
            await message.channel.send(None, embed=embed)
            return
        cmd.db.take_points(message.guild, message.author, bet_amt)
        embed_colors = [0x990000, 0x0066FF, 0x009900, 0xff9900, 0xCC33FF, 0x990033]
        slot_embed = discord.Embed(color=random.choice(embed_colors))
        slot_back_data.update({message.author.id: current_time})
        rand_done = 0
        res_1 = random.choice(symbols)
        res_2 = random.choice(symbols)
        res_3 = random.choice(symbols)
        res_4 = random.choice(symbols)
        res_5 = random.choice(symbols)
        res_6 = random.choice(symbols)
        res_7 = random.choice(symbols)
        res_8 = random.choice(symbols)
        res_9 = random.choice(symbols)

        slot_view = '⏸ ' + res_4 + ' ' + res_5 + ' ' + res_6 + ' ⏸'
        slot_view += '\n▶ ' + res_1 + ' ' + res_2 + ' ' + res_3 + ' ◀'
        slot_view += '\n⏸ ' + res_7 + ' ' + res_8 + ' ' + res_9 + ' ⏸'
        slot_embed.add_field(name='🎰 Slots are spinning...', value=slot_view)
        slot_spinner = await message.channel.send(None, embed=slot_embed)
        spin_amt = random.randint(min_spins, max_spins)
        while rand_done < spin_amt:
            await asyncio.sleep(spin_cycle_timeout)
            rand_done += 1
            res_7 = res_1
            res_8 = res_2
            res_9 = res_3
            res_1 = res_4
            res_2 = res_5
            res_3 = res_6
            res_4 = random.choice(symbols)
            res_5 = random.choice(symbols)
            res_6 = random.choice(symbols)
            slot_view = '⏸ ' + res_4 + ' ' + res_5 + ' ' + res_6 + ' ⏸'
            slot_view += '\n▶ ' + res_1 + ' ' + res_2 + ' ' + res_3 + ' ◀'
            slot_view += '\n⏸ ' + res_7 + ' ' + res_8 + ' ' + res_9 + ' ⏸'
            slot_embed.set_field_at(0, name='🎰 Slots are spinning...', value=slot_view)
            await slot_spinner.edit(embed=slot_embed)

        # Result Response
        subtext = ''
        if res_1 == res_2 == res_3:
            win = True
            pts = bet_amt * 210
            subtext += 'Your major victory has been recorded on the `#slot-wins` channel of Sigma\'s official server.'
            win_notify_channel_object = None
            for server in cmd.bot.guilds:
                for channel in server.channels:
                    if channel.id == SlotWinChannelID:
                        win_notify_channel_object = channel
                        break
            if SlotWinChannelID:
                win_notify_embed = discord.Embed(color=0x0099FF, title='💎 We have a winner!')
                win_notify_embed.add_field(name='User', value=message.author.name)
                win_notify_embed.add_field(name='Server', value=message.guild.name)
                embed_icon = message.author.default_avatar_url
                if message.author.avatar_url != '':
                    embed_icon = message.author.avatar_url
                win_notify_embed.set_thumbnail(url=embed_icon)
                await win_notify_channel_object.send(None, embed=win_notify_embed)
        elif res_1 == res_2 or res_1 == res_3 or res_2 == res_3:
            win = True
            pts = bet_amt * 12
        else:
            win = False
            pts = 0
        if win:
            cmd.db.add_points(message.guild, message.author, pts)
            slot_embed.set_field_at(0, name='💎 You Won!', value=slot_view)
            slot_embed.set_footer(text='You won ' + str(pts) + ' points.')
            await slot_spinner.edit(embed=slot_embed)
        else:
            slot_embed.set_field_at(0, name='💣 You Lost...', value=slot_view)
            slot_embed.set_footer(text='You lost the ' + str(bet_amt) + ' points that you bet.')
            await slot_spinner.edit(embed=slot_embed)
    else:
        cd_timestamp = slot_back_data[message.author.id]
        current_time = arrow.utcnow().timestamp
        timeout_amt = cd_timestamp + 60 - current_time
        embed = discord.Embed(color=0xDB0000,
                              title='❗ You can\'t spin for another ' + str(timeout_amt) + ' seconds!')
        await message.channel.send(embed=embed)
        return
