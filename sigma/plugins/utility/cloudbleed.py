import discord
import aiohttp


async def cloudbleed(cmd, message, args):
    if args:
        url = 'https://api.auroraproject.xyz/api/v1/cloudbleed?qry=' + ' '.join(args)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as data:
                data = await data.json()
        if len(data['urls']) == 0:
            embed = discord.Embed(color=0x66CC66, title='✅ Not Found')
            embed.set_footer(text='This is a good thing.')
        else:
            result_text = ', '.join(data['urls'][:20])
            embed = discord.Embed(color=0xf48220)
            embed.add_field(name=':syringe: Websites found matching that search.', value=f'```\n{result_text}\n```')
        await message.channel.send(None, embed=embed)
