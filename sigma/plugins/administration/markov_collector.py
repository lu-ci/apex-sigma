import os
import yaml
from config import Prefix

async def markov_collector(ev, message, args):
    if message.server:
        if not message.author.bot:
            collect = ev.db.get_settings(message.server.id, 'MarkovCollect')
            if message.content != '' and not message.content.startswith(Prefix):
                if collect:
                    directory = 'chains/'
                    filename = f'chain_{message.server.id}_{message.author.id}.yml'
                    chain_location = f'{directory}{filename}'
                    if os.path.exists(chain_location):
                        with open(chain_location) as chain_file:
                            chain_data = yaml.safe_load(chain_file)
                        chain_data.append(message.content)
                        with open(chain_location, 'w') as chain_file:
                            yaml.dump(chain_data, chain_file, default_flow_style=False)
                    else:
                        chain_data = [message.content]
                        with open(chain_location, 'w') as chain_file:
                            yaml.dump(chain_data, chain_file, default_flow_style=False)
