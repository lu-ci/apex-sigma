import chatterbot
import yaml

with open('VERSION') as version_file:
    data = yaml.load(version_file)
    codename = data['codename']

sigma = chatterbot.ChatBot(
    codename,
    logic_adapters=[
        {
            "import_path": "chatterbot.logic.BestMatch"
        },
        {
            "import_path": "chatterbot.logic.MathematicalEvaluation"
        },
        {
            "import_path": "chatterbot.logic.TimeLogicAdapter"
        },
    ],
    database='./chatterbot.db'
)
sigma.initialize()

async def cleverbot_control(ev, message, args):
    active = ev.db.get_settings(message.server.id, 'CleverBot')
    if active:
        ev.db.add_stats('CBCount')
        mention = '<@' + ev.bot.user.id + '>'
        mention_alt = '<@!' + ev.bot.user.id + '>'
        if message.content.startswith(mention) or message.content.startswith(mention_alt):
            response = sigma.get_response(' '.join(args[1:]))
            await ev.bot.send_message(message.channel, response)
