import yaml
import discord
from config import Prefix

in_use = False

async def collectchain(cmd, message, args):
    global in_use
    if in_use:
        response = discord.Embed(color=0x696969, title='🛠 Currently in use. Try Again Later.')
        await cmd.bot.send_message(message.channel, None, embed=response)
    else:
        if args:
            if message.mentions:
                target = message.mentions[0]
            else:
                target = discord.utils.find(lambda x: x.name.lower() == ' '.join(args).lower(), message.server.members)
            if target:
                def_chn = message.server.default_channel
                collected = 0
                collection = []
                in_use = True
                response = discord.Embed(color=0x66CC66, title='📖 Collecting...')
                response_msg = await cmd.bot.send_message(message.channel, None, embed=response)
                async for log in cmd.bot.logs_from(def_chn, limit=50000):
                    if log.author.id == target.id:
                        if log.content:
                            if log.content != '':
                                if len(log.content) > 3:
                                    if not log.content.startswith(Prefix):
                                        if 'http' not in log.content and '```' not in log.content:
                                            content = log.content
                                            if log.mentions:
                                                for mention in log.mentions:
                                                    content = content.replace(mention.mention, mention.name)
                                            if log.channel_mentions:
                                                for mention in log.channel_mentions:
                                                    content = content.replace(mention.mention, mention.name)
                                            unallowed_chars = ['`', '\n', '\\', '\\n']
                                            for char in unallowed_chars:
                                                content = content.replace(char, '')
                                            if len(content) > 48:
                                                if not content.endswith(('.' or '?' or '!')):
                                                    content += '.'
                                            collection.append(content)
                                            collected += 1
                                            if collected >= 3000:
                                                break
                with open(f'chains/chain_{target.id}.yml', 'w', encoding='utf-8') as chain_file:
                    yaml.dump(collection, chain_file, default_flow_style=False)
                in_use = False
                response = discord.Embed(color=0x66CC66, title='📖 Done!')
                await cmd.bot.edit_message(response_msg, None, embed=response)
