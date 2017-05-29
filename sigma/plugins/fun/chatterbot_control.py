from chatterbot import ChatBot
from config import MongoAuth, MongoAddress, MongoPort, MongoUser, MongoPass

if MongoAuth:
    db_url = f'mongodb://{MongoUser}:{MongoPass}@{MongoAddress}:{MongoPort}/'
else:
    db_url = f'mongodb://{MongoAddress}:{MongoPort}/'

cb = ChatBot(
    'Sigma',
    storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
    database='chatterbot',
    database_uri=db_url,
    output_adapter='chatterbot.output.OutputAdapter',
    output_format='text',
    read_only=False
)

async def chatterbot_control(ev, message, args):
    active = ev.db.get_settings(message.guild.id, 'CleverBot')
    if active:
        ev.db.add_stats('CBCount')
        mention = f'<@{ev.bot.user.id}>'
        mention_alt = f'<@!{ev.bot.user.id}>'
        if message.content.startswith(mention) or message.content.startswith(mention_alt):
            interaction = ' '.join(args[1:])
            if message.mentions:
                for mnt in message.mentions:
                    interaction = interaction.replace(mnt.mention, mnt.name)
            response = str(cb.get_response(interaction))
            await message.channel.send(message.author.mention + ' ' + response)
