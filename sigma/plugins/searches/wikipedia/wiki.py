import wikipedia
import discord


async def wiki(cmd, message, args):
    q = ' '.join(args).lower()
    result = wikipedia.summary(q)
    if len(result) >= 650:
        result = result[:650] + '...'
    embed = discord.Embed(color=0x1abc9c)
    embed.add_field(name='Wikipedia Search For `' + q + '`', value='```\n' + result + '\n```')
    await message.channel.send(None, embed=embed)
