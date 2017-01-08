import hashlib
import discord


async def md5(cmd, message, args):
    if not args:
        embed = discord.Embed(color=0xDB0000, title=':exclamation: Nothing to hash.')
        await cmd.bot.send_message(message.channel, None, embed=embed)
        return
    qry = ' '.join(args)
    crypt = hashlib.md5()
    crypt.update(qry.encode('utf-8'))
    final = crypt.hexdigest()
    embed = discord.Embed(color=0x66cc66)
    embed.add_field(name=':white_check_mark: Hashing Done', value='```\n' + final + '\n```')
    await cmd.bot.send_message(message.channel, None, embed=embed)
