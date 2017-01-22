import discord
import pymarkovchain


async def qme(cmd, message, args):
    chain = pymarkovchain.MarkovChain(cmd.resource('owner_markov_chain'))
    output = chain.generateString()
    embed = discord.Embed(color=0x1abc9c)
    embed.add_field(name='㊙ Bot Owner Says', value='```\n' + output + '\n```')
    await cmd.bot.send_message(message.channel, None, embed=embed)
