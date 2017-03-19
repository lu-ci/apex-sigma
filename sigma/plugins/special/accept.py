import asyncio
import discord
from config import permitted_id


async def accept(ev, message, args):
    if message.channel.id == '225375071349243904':
        give_role = None
        for role in message.server.roles:
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
            await ev.bot.add_roles(message.author, give_role)
            for member in message.server.members:
                if member.id == permitted_id[0]:
                    embed = discord.Embed(
                        title='ℹ ' + message.author.name + ' has accepted the terms on WKCD.',
                        color=0x0099FF)
                    await ev.bot.send_message(member, None, embed=embed)
            for channel in message.server.channels:
                if channel.is_default:
                    await ev.bot.send_message(channel,
                                              'Hello <@' + message.author.id + '>! Welcome to the WaniKani Community Discord Server! If you wanna chat, feel bored, need help with your Nihongo or whatever crosses your mind, you are welcome to chat about it here~ If you encounter any problems be sure to say so to a moderator! The pinned messages in each channel will have some info as well\nようこそ！もし日本語でしゃべりたければ、音声チャネルにご参加ください！')
        elif message.content == '>>decline':
            response = await ev.bot.send_message(message.channel,
                'We are sorry to hear that.\nYou will be removed from the server shortly.\nBon voyage~')
            await asyncio.sleep(5)
            await ev.bot.kick(message.author)
            await ev.bot.delete_message(response)
        asyncio.sleep(10)
        await ev.bot.delete_message(message)
