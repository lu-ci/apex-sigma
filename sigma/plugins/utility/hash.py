import hashlib
import discord


async def hash(cmd, message, args):
    if not args:
        embed = discord.Embed(color=0xDB0000, title=':exclamation: No hash inputted and nothing to hash.')
        await cmd.bot.send_message(message.channel, None, embed=embed)
        return
    if len(args) < 2:
        embed = discord.Embed(color=0xDB0000, title=':exclamation: Nothing to hash.')
        await cmd.bot.send_message(message.channel, None, embed=embed)
        return
    hash_name = args[0]
    hashes = hashlib.algorithms_available
    if hash_name not in hashes:
        embed = discord.Embed(color=0xDB0000)
        embed.add_field(name=':exclamation: Unknown Hashing Method',
                        value='Available:\n```\n' + ', '.join(hashes) + '\n```')
        await cmd.bot.send_message(message.channel, None, embed=embed)
        return
    qry = ' '.join(args[1:])
    crypt = hashlib.new(hash_name)
    crypt.update(qry.encode('utf-8'))
    final = crypt.hexdigest()
    embed = discord.Embed(color=0x66cc66)
    embed.add_field(name=':white_check_mark: Hashing With ' + hash_name.upper() + ' Done',
                    value='```\n' + final + '\n```')
    await cmd.bot.send_message(message.channel, None, embed=embed)
