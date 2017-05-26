from config import Prefix
from sigma.core.blacklist import check_black


async def custom_command_detection(ev, message, args):
    if message.guild:
        if message.content.startswith(Prefix):
            cmd = message.content[len(Prefix):].lower()
            if cmd not in ev.bot.plugin_manager.commands:
                if not check_black(ev.db, message):
                    try:
                        custom_commands = ev.db.get_settings(message.guild.id, 'CustomCommands')
                    except:
                        ev.db.set_settings(message.guild.id, 'CustomCommands', {})
                        custom_commands = {}
                    if cmd in custom_commands:
                        response = custom_commands[cmd]
                        await message.channel.send(response)
