import discord
import requests


async def cloudbleed(cmd, message, args):
    if args:
        url = 'https://cloudbleed-api.whats-th.is/api/v1/search?query=' + ' '.join(args)
        data = requests.get(url).json()
        if len(data['items']) == 0:
            embed = discord.Embed(color=0x66CC66, title=':white_check_mark: Not Found')
            embed.set_footer(text='This is a good thing.')
        else:
            result_text = ', '.join(data['items'][:20])
            embed = discord.Embed(color=0xf48220)
            embed.add_field(name=':syringe: Websites found matching that search.', value=f'```\n{result_text}\n```')
        await cmd.bot.send_message(message.channel, None, embed=embed)
