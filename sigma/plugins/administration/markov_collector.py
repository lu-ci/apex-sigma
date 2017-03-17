import pymarkovchain

async def markov_collector(ev, message, args):
    collect = ev.db.get_settings(message.server.id, 'MarkovCollect')
    if message.content != '':
        if collect:
            directory = 'chains/'
            chain = pymarkovchain.MarkovChain(directory + message.server.id)
            chain.generateDatabase(message.content)
            chain.dumpdb()
