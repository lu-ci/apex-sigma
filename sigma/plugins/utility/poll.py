import discord
import random


async def poll(cmd, message, args):
    if not args:
        out_content = discord.Embed(type='rich', color=0xDB0000,
                                    title=':exclamation: Missing Arguments.')
        await cmd.bot.send_message(message.channel, None, embed=out_content)
        return
    all_qry = ' '.join(args)
    if all_qry.endswith(';'):
        all_qry = all_qry[:-1]
    poll_name = all_qry.split('; ')[0]
    choice_qry = ' '.join(args[1:])
    if choice_qry.endswith(';'):
        choice_qry = choice_qry[:-1]
    poll_choices = choice_qry.split('; ')
    if len(poll_choices) < 2:
        out_content = discord.Embed(type='rich', color=0xDB0000,
                                    title=':exclamation: Not enough arguments choice present.')
        await cmd.bot.send_message(message.channel, None, embed=out_content)
        return
    if len(poll_choices) > 9:
        out_content = discord.Embed(type='rich', color=0xDB0000,
                                    title=':exclamation: Maximum is 9 choices.')
        await cmd.bot.send_message(message.channel, None, embed=out_content)
        return
    icon_list_base = ['🍏', '🍍', '🍐', '🌶', '🍆', '🍋', '🍌', '🍅', '🍓', '🍇']
    random.shuffle(icon_list_base, random.random)
    choice_text = ''
    op_num = 0
    for option in poll_choices:
        choice_text += '\n' + icon_list_base[op_num] + ' - **' + option + '**'
        op_num += 1
    out_content = discord.Embed(color=0x1ABC9C)
    out_content.add_field(name=poll_name, value=choice_text)
    poll_message = await cmd.bot.send_message(message.channel, None, embed=out_content)
    ic_num = 0
    for option in poll_choices:
        emoji = icon_list_base[ic_num]
        await cmd.bot.add_reaction(poll_message, emoji=emoji)
        ic_num += 1
