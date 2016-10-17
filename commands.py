import json

with open('commands.json', 'r', encoding='utf-8') as commands_file:
    commands = commands_file.read()
    commands = json.loads(commands)
    print('Loaded commands.')

# Commands
cmd_help = (commands['cmd_help'])
cmd_overwatch = (commands['cmd_overwatch'])
cmd_league = (commands['cmd_league'])
cmd_bns = (commands['cmd_bns'])
cmd_ud = (commands['cmd_ud'])
cmd_weather = (commands['cmd_weather'])
cmd_hearthstone = (commands['cmd_hearthstone'])
cmd_pokemon = (commands['cmd_pokemon'])
cmd_joke = (commands['cmd_joke'])
cmd_echo = 'echo'