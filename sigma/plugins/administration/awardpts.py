import discord
from config import Currency


async def awardpts(cmd, message, args):
    if message.mentions:
        target = message.mentions[0]
        if target.bot:
            out = discord.Embed(title='❗ Can\'t award bots.', color=0xDB0000)
            await message.channel.send(None, embed=out)
            return
        try:
            amount = abs(int(args[0]))
        except:
            out = discord.Embed(title='❗ Invalid Input.', color=0xDB0000)
            await message.channel.send(None, embed=out)
            return
        cmd.db.add_points(message.guild, target, amount)
        out = discord.Embed(title='✅ Done', color=0x66CC66)
        out.add_field(name='Sent To', value=f'```py\n{target.name}#{target.discriminator}\n```')
        out.add_field(name='Amount', value=f'```py\n{amount} {Currency}\n```')
        await message.channel.send(None, embed=out)
        try:
            out = discord.Embed(title=f'💎 You Were Given {Currency}', color=0x0099FF)
            out.add_field(name='Server', value=f'```\n{message.guild.name}\n```')
            out.add_field(name='From', value=f'```py\n{message.author.name}#{message.author.discriminator}\n```')
            out.add_field(name='Amount', value=f'```py\n{amount} {Currency}\n```')
            await cmd.bot.send_message(target, None, embed=out)
        except:
            pass
    else:
        await message.channel.send(cmd.help())
