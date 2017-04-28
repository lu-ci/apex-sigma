import wolframalpha
import discord
from config import WolframAlphaAppID


async def wa(cmd, message, args):
    if not args:
        await message.channel.send(cmd.help())
        return
    else:
        wa_q = ' '.join(args)
        wac = wolframalpha.Client(WolframAlphaAppID)
        results = wac.query(wa_q)
        try:
            out_content = discord.Embed(type='rich', color=0x66cc66, title='✅ Processing Done')
            for res in results.results:
                if int(res['@numsubpods']) == 1:
                    out_content.add_field(name=res['@title'],
                                          value='```\n' + res['subpod']['plaintext'][:1950] + '\n```')
                else:
                    out_content.add_field(name=res['@title'],
                                          value='```\n' + res['subpod'][0]['img']['@title'][:1950] + '\n```')
        except Exception as e:
            cmd.log.error(e)
            out_content = discord.Embed(type='rich', color=0xDB0000,
                                        title=':bug: We ran into an error, we were unable to process that.')
            await message.channel.send(None, embed=out_content)
            return
        await message.channel.send(None, embed=out_content)
