import os
import discord
import markovify
import yaml


async def markov(cmd, message, args):
    collect = cmd.db.get_settings(message.server.id, 'MarkovCollect')
    if collect:
        directory = 'chains/'
        filename = f'chain_{message.server.id}.yml'
        chain_location = f'{directory}{filename}'
        if os.path.exists(chain_location):
            with open(chain_location) as chain_file:
                chain_data = yaml.safe_load(chain_file)
                entire_data = ' '.join(chain_data)
                chain = markovify.Text(entire_data)
                output = f'{chain.make_short_sentence(140)}'
                for member in cmd.bot.get_all_members():
                    output = output.replace(f'<@!{member.id}', member.name)
                    output = output.replace(f'<@{member.id}', member.name)
                    output = output.replace(member.id, member.name)
                response = discord.Embed(color=0x1ABC9C)
                response.add_field(name=f':link: {message.server.name} Markov Chain Response',
                                   value=f'```\n{output}\n```')
        else:
            response = discord.Embed(color=0xDB0000, title='⛔ No Chain File Was Found')
    else:
        response = discord.Embed(color=0xDB0000,
                                 title=f'⛔ Markov Collection Is Disabled on {message.server.name}')
    await message.channel.send(None, embed=response)
