import discord
import translate as trans


async def translate(cmd, message, args):
    if not args:
        embed = discord.Embed(color=0xDB0000, title='❗ No Arguments Given')
    else:
        trans_qry = args[0]
        if '>' not in trans_qry:
            embed = discord.Embed(color=0xDB0000, title='❗ Invalid Translation Query')
        else:
            to_trans = ' '.join(args[1:])
            from_lang, to_lang = trans_qry.split('>')
            translator = trans.Translator(from_lang=from_lang, to_lang=to_lang)
            transed = translator.translate(to_trans)
            embed = discord.Embed(color=0x1abc9c, title='📚 Translated')
            embed.add_field(name=f'From {from_lang.upper()}', value=f'```\n{to_trans}\n```', inline=False)
            embed.add_field(name=f'To {to_lang.upper()}', value=f'```\n{transed}\n```', inline=False)
    await message.channel.send(None, embed=embed)
