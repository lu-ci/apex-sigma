import arrow
import discord


async def afk(cmd, message, args):
    afk_data = cmd.db.find_one('AwayUsers', {'UserID': message.author.id})
    if afk_data:
        response = discord.Embed(color=0xDB0000, title='❗ You are already marked as AFK.')
    else:
        afk_reason = ' '.join(args)
        in_data = {
            'UserID': message.author.id,
            'Timestamp': arrow.utcnow().timestamp,
            'Reason': afk_reason
        }
        cmd.db.insert_one('AwayUsers', in_data)
        response = discord.Embed(color=0x66CC66)
        response.add_field(name='✅ You have been marked as afk.', value=f'Reason: {afk_reason}')
    await message.channel.send(embed=response)
