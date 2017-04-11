import asyncio
import aiohttp
import discord


async def setavatar(cmd, message, args):
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
                    await cmd.bot.user.edit(avatar=await res.read())
                    embed = discord.Embed(title='✅ New Avatar Set', color=0x66CC66)
                    await message.channel.send(None, embed=embed)
                    await aiosession.close()
        except Exception as e:
            cmd.log.error(e)
            return
    except AttributeError:
        try:
            thing = ''.join(args)

            try:
                with aiohttp.Timeout(10):
                    async with aiosession.get(thing) as res:
                        await cmd.bot.user.edit(avatar=await res.read())
                        embed = discord.Embed(title='✅ New Avatar Set', color=0x66CC66)
                        await message.channel.send(None, embed=embed)
            except:
                return
        except ResourceWarning:
            pass
        except Exception as e:
            embed = discord.Embed(color=0xDB0000)
            embed.add_field(name='❗ Error', value=str(e))
            await message.channel.send(None, embed=embed)
