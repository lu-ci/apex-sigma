import discord
from sigma.core.permission import check_admin
from config import Prefix


async def eventchance(cmd, message, args):
    if not check_admin(message.author, message.channel):
        out_content = discord.Embed(type='rich', color=0xDB0000,
                                    title=':no_entry: Insufficient Permissions. Server Admin Only.')
        await cmd.bot.send_message(message.channel, None, embed=out_content)
        return
    events_enabled = cmd.db.get_settings(message.server.id, 'RandomEvents')
    event_chance = cmd.db.get_settings(message.server.id, 'EventChance')
    if not args:
        out_content = discord.Embed(color=0x0099FF,
                                    title=':information_source: Random Event Chance Is ' + str(event_chance) + '%')
        if not events_enabled:
            out_content.set_footer(text='Warning: Random Events Are Disabled, use ' + Prefix + 'events to toggle it.')
        await cmd.bot.send_message(message.channel, None, embed=out_content)
    if args:
        new_chance = args[0]
        try:
            new_chance = int(new_chance)
        except:
            out_content = discord.Embed(type='rich', color=0xDB0000,
                                        title=':exclamation: Invalid Number Input.')
            await cmd.bot.send_message(message.channel, None, embed=out_content)
            return
        if new_chance > 100:
            new_chance = 100
        if new_chance < 1:
            new_chance = 1
        cmd.db.set_settings(message.server.id, 'EventChance', new_chance)
        out = discord.Embed(title='✅ Event Chance Set to ' + str(new_chance) + '%', color=0x66CC66)
        await cmd.bot.send_message(message.channel, None, embed=out)
