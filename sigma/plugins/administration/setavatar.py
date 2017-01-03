import asyncio
import aiohttp
import discord

from config import permitted_id


async def setavatar(cmd, message, args):
    if message.author.id in permitted_id:
        loop = asyncio.get_event_loop()
        aiosession = aiohttp.ClientSession(loop=loop)

        url = ''.join(args)

        try:
            if message.attachments:
                thing = message.attachments[0]['url']
            else:
                thing = url.strip('<>')
            try:
                with aiohttp.Timeout(10):
                    async with aiosession.get(thing) as res:
                        await cmd.bot.edit_profile(avatar=await res.read())
                        embed = discord.Embed(title=':white_check_mark: New Avatar Set', color=0x66CC66)
                        await cmd.bot.send_message(message.channel, None, embed=embed)
            except Exception as e:
                cmd.log.error(e)
                return
        except AttributeError:
            try:
                thing = ''.join(args)

                try:
                    with aiohttp.Timeout(10):
                        async with aiosession.get(thing) as res:
                            await cmd.bot.edit_profile(avatar=await res.read())
                            embed = discord.Embed(title=':white_check_mark: New Avatar Set', color=0x66CC66)
                            await cmd.bot.send_message(message.channel, None, embed=embed)
                except:
                    return
            except ResourceWarning:
                pass
            except Exception as e:
                embed = discord.Embed(color=0xDB0000)
                embed.add_field(name=':exclamation: Error', value=str(e))
                await cmd.bot.send_message(message.channel, None, embed=embed)

    else:
        out = discord.Embed(type='rich', color=0xDB0000,
                            title=':no_entry: Insufficient Permissions. Bot Owner Only.')
        await cmd.bot.send_message(message.channel, None, embed=out)
