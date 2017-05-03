import asyncio
import discord
from config import permitted_id


async def accept(ev, message, args):
    if message.channel.id == 225375071349243904:
        give_role = None
        for role in message.guild.roles:
            if role.name == 'Crabigator\'s Pet':
                give_role = role
            else:
                pass
        if not give_role:
            return
        for role in message.author.roles:
            if role.name == 'Crabigator\'s Pet':
                return
        if message.content == '>>accept':
            await message.author.add_roles(give_role)
            embed = discord.Embed(
                title='ℹ ' + message.author.name + ' has accepted the terms on WKCD.',
                color=0x0099FF)
            owner = discord.utils.find(lambda x: x.id == permitted_id[0], ev.bot.get_all_members())
            await owner.send(None, embed=embed)
            notify_channel = discord.utils.find(lambda x: x.id == 219894896172072971, ev.bot.get_all_channels())
            await notify_channel.send(
                f'Hello <@{message.author.id}>! Welcome to the WaniKani Community Discord Server! If you wanna chat, feel bored, need help with your Nihongo or whatever crosses your mind, you are welcome to chat about it here~ If you encounter any problems be sure to say so to a moderator! The pinned messages in each channel will have some info as well\nようこそ！もし日本語でしゃべりたければ、音声チャネルにご参加ください！')
        elif message.content == '>>decline':
            response = await message.channel.send(
                'We are sorry to hear that.\nYou will be removed from the server shortly.\nBon voyage~')
            await asyncio.sleep(5)
            await message.author.kick()
            await response.delete()
        asyncio.sleep(10)
        await message.delete()
