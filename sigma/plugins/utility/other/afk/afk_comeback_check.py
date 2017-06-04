import discord
from config import Prefix


async def afk_comeback_check(ev, message, args):
    if message.guild:
        if not message.content.startswith(Prefix):
            afk_data = ev.db.find_one('AwayUsers', {'UserID': message.author.id})
            if afk_data:
                ev.db.delete_one('AwayUsers', {'UserID': message.author.id})
                response = discord.Embed(color=0x0099FF, title='ℹ I have removed your AFK status.')
                await message.channel.send(embed=response)
