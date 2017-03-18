import os
import yaml
import discord
import markovify


async def markov(cmd, message, args):
    collect = cmd.db.get_settings(message.server.id, 'MarkovCollect')
    if collect:
        directory = 'chains/'
        filename = f'chain_{message.server.id}.yml'
        chain_location = f'{directory}{filename}'
        if os.path.exists(chain_location):
            with open(chain_location) as chain_file:
                chain_data = yaml.safe_load(chain_file)
                entire_data = '. '.join(chain_data)
                text_model = markovify.Text(entire_data)
                output = text_model.make_sentence()
                response = discord.Embed(color=0x1ABC9C)
                response.add_field(name=f':link: {message.server.name} Markov Chain Response',
                                   value=f'```\n{output}\n```')
        else:
            response = discord.Embed(color=0xDB0000, title=':no_entry: No Chain File Was Found')
    else:
        response = discord.Embed(color=0xDB0000,
                                 title=f':no_entry: Markov Collection Is Disabled on {message.server.name}')
    await cmd.bot.send_message(message.channel, None, embed=response)
