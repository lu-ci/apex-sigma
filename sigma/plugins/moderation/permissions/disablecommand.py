import discord
from sigma.core.permission import check_admin
from .nodes.permission_data import get_all_perms

async def disablecommand(cmd, message, args):
    if args:
        if not check_admin(message.author, message.channel):
            response = discord.Embed(title='⛔ Unpermitted. Server Admin Only.', color=0xDB0000)
        else:
            cmd_name = args[0].lower()
            if cmd_name in cmd.bot.alts:
                cmd_name = cmd.bot.alts[cmd_name]
            if cmd_name in cmd.bot.plugin_manager.commands:
                perms = get_all_perms(cmd.db, message)
                disabled_commands = perms['DisabledCommands']
                if cmd_name in disabled_commands:
                    response = discord.Embed(color=0xFF9900, title='⚠ Command Already Disabled')
                else:
                    disabled_commands.append(cmd_name)
                    perms.update({'DisabledCommands': disabled_commands})
                    cmd.db.update_one('Permissions', {'ServerID': message.guild.id}, {'$set': perms})
                    response = discord.Embed(color=0x66CC66, title=f'✅ `{cmd_name.upper()}` disabled.')
            else:
                response = discord.Embed(color=0x696969, title='🔍 Command Not Found')
        await message.channel.send(embed=response)
