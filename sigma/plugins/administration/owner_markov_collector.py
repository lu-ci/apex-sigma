from config import permitted_id, Prefix
import pymarkovchain


async def owner_markov_collector(ev, message, args):
    if message.author.id in permitted_id:
        if message.content and message.content != '':
            if not message.content.startswith(Prefix):
                chain = pymarkovchain.MarkovChain(ev.resource('owner_markov_chain'))
                chain.generateDatabase(message.content)
                chain.dumpdb()
