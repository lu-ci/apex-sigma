import discord
from sigma.core.permission import check_man_srv


async def addcommand(cmd, message, args):
    if check_man_srv(message.author, message.channel):
        if args:
            if len(args) >= 2:
                trigger = args[0].lower()
                if trigger not in cmd.bot.plugin_manager.commands and trigger not in cmd.bot.alts:
                    content = ' '.join(args[1:])
                    try:
                        custom_commands = cmd.db.get_settings(message.guild.id, 'CustomCommands')
                    except:
                        cmd.db.set_settings(message.guild.id, 'CustomCommands', {})
                        custom_commands = {}
                    if trigger in custom_commands:
                        res_text = 'updated'
                    else:
                        res_text = 'added'
                    custom_commands.update({trigger: content})
                    cmd.db.set_settings(message.guild.id, 'CustomCommands', custom_commands)
                    response = discord.Embed(title=f'✅ {trigger} has been {res_text}', color=0x66CC66)
                else:
                    response = discord.Embed(title='❗ Can\'t replace an existing core command', color=0xDB0000)
            else:
                response = discord.Embed(title='❗ Missing Message To Send', color=0xDB0000)
        else:
            response = discord.Embed(title='❗ Nothing Was Inputted', color=0xDB0000)
    else:
        response = discord.Embed(title='⛔ Unpermitted. Server Admin Only.', color=0xDB0000)
    await message.channel.send(embed=response)
