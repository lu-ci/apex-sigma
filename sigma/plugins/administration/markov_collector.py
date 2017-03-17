import pymarkovchain
from config import Prefix

async def markov_collector(ev, message, args):
    if message.server:
        if not message.author.bot:
            collect = ev.db.get_settings(message.server.id, 'MarkovCollect')
            if message.content != '' and not message.content.startswith(Prefix):
                if collect:
                    directory = 'chains/'
                    chain = pymarkovchain.MarkovChain(directory + message.server.id)
                    chain.generateDatabase(message.content)
                    chain.dumpdb()
