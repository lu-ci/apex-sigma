from config import permitted_id
import pymarkovchain


async def owner_markov_collector(ev, message, args):
    if message.content and message.content != '':
        chain = pymarkovchain.MarkovChain(ev.resource('owner_markov_chain'))
        chain.generateDatabase(message.content)
        chain.dumpdb()
