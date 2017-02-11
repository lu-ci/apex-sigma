import chatterbot
import yaml
from config import Prefix

with open('VERSION') as version_file:
    data = yaml.load(version_file)
    codename = data['codename']

sigma = chatterbot.ChatBot(
    codename,
    trainer='chatterbot.trainers.ListTrainer',
    database='./chatterbot.db'
)

train_dict = {}


async def chatter_trainer(ev, message, args):
    if not message.author.bot:
        if not message.content.startswith(Prefix):
            if message.server:
                global train_dict
                train_list = []
                if message.channel.id in train_dict:
                    train_list = train_dict[message.channel.id]
                list_length = len(train_list)
                text_data = message.content
                if message.mentions:
                    for mention in message.mentions:
                        text_data.replace(mention.mention, '')
                text_data = text_data.replace('  ', ' ')
                if list_length < 50:
                    train_list.append(text_data)
                else:
                    sigma.trainer.train(train_list)
                    ev.log.info('New Training Data Recorded')
                    train_list = [text_data]
                train_dict.update({message.channel.id: train_list})
