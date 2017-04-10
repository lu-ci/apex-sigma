import discord
from .nodes.read_scroll_data import search_for_scroll


async def enchantscroll(cmd, message, args):
    if args:
        scroll_name = '_'.join(args).title()
        try:
            scroll = await search_for_scroll(scroll_name)
            response = discord.Embed(color=0xB38000)
            response.set_author(name=scroll.name, icon_url=scroll.icon)
            info_text = f'Rank: {scroll.rank}\nType: {scroll.type}\nEquipment: {scroll.target}'
            if scroll.other:
                info_text += f'\nSuccess Chance: {scroll.other.success_chance}'
                info_text += f'\nDestruction Chance: {scroll.other.destruction_chance}'
            response.add_field(name='ℹ Information', value=f'```\n{info_text}\n```', inline=False)
            enchant_text = 'Unknown'
            if scroll.stats:
                enchant_text = ''
                for stat in scroll.stats:
                    enchant_text += f'\n- {stat}'
            response.add_field(name=f'🌟 Enchantment: {scroll.enchant}', value=f'```\n{enchant_text}\n```',
                               inline=False)
            if scroll.other:
                drop_locations = 'Unknown'
                if scroll.other.drop_locations:
                    drop_locations = ''
                    for location in scroll.other.drop_locations:
                        drop_locations += f'\n- {location}'
                response.add_field(name='🗺 Drop Locations', value=f'```\n{drop_locations}\n```', inline=False)
        except:
            response = discord.Embed(color=0x696969, title='🔍 Nothing Found')
        await message.channel.send(None, embed=response)
