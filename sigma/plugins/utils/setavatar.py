import asyncio
import aiohttp

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
                except:
                    return
            except ResourceWarning:
                pass
            except Exception as e:
                await cmd.reply(e)
