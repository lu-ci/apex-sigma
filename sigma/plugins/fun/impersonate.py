from sigma.core.utils import user_avatar
from config import Prefix
import markovify
import discord
import ftfy


async def impersonate(cmd, message, args):
    if args:
        if message.mentions:
            target = message.mentions[0]
        else:
            target = discord.utils.find(lambda x: x.name.lower() == ' '.join(args).lower(), message.guild.members)
        if target:
            chain_data = cmd.db.find_one('MarkovChains', {'UserID': target.id})
            if chain_data:
                total_string = ' '.join(chain_data['Chain'])
                total_string = ftfy.fix_text(total_string)
                chain = markovify.Text(total_string)
                sentence = chain.make_sentence(tries=100)
                if not sentence:
                    response = discord.Embed(color=0xDB0000, title='😖 I Couldn\'t think of anything...')
                else:
                    sentence = ftfy.fix_text(sentence)
                    response = discord.Embed(color=0x1ABC9C)
                    response.set_author(name=target.name, icon_url=user_avatar(target))
                    response.add_field(name='🤔 Something like...', value=f'```\n{sentence}\n```')
            else:
                response = discord.Embed(color=0x696969)
                response.add_field(name=f'🔍 Chain Data Not Found For {target.name}',
                                   value=f'You can make one with `{Prefix}collectchain @{target.name} #channel`!')
            await message.channel.send(None, embed=response)
