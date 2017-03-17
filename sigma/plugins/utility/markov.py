import os
import discord
import pymarkovchain


async def markov(cmd, message, args):
    collect = cmd.db.get_settings(message.server.id, 'MarkovCollect')
    if collect:
        directory = 'chains/'
        location = directory + message.server.id
        if os.path.exists(location):
            chain = pymarkovchain.MarkovChain(location)
            output = chain.generateString()
            response = discord.Embed(color=0x1abc9c)
            response.add_field(name=f':link: {message.server.name} Markov Chain Response', value=f'```\n{output}\n```')
        else:
            response = discord.Embed(color=0xDB0000, title=':no_entry: No Chain File Was Found')
    else:
        response = discord.Embed(color=0xDB0000,
                                 title=f':no_entry: Markov Collection Is Disabled on {message.server.name}')
    await cmd.bot.send_message(message.channel, None, embed=response)
