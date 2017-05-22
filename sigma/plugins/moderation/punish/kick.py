from sigma.core.permission import check_kick
import discord


async def kick(cmd, message, args):
    if not check_kick(message.author, message.channel):
        response = discord.Embed(title='⛔ Unpermitted. Kick Permissions Needed.', color=0xDB0000)
    else:
        if message.mentions:
            target = message.mentions[0]
            if target.id == message.author.id:
                response = discord.Embed(title='⛔ You can\'t kick yourself.', color=0xDB0000)
            else:
                await target.kick(reason=f'Kicked by {message.author.name}#{message.author.discriminator}.')
                response = discord.Embed(title=f'👢 {target.name} has been kicked.')
        else:
            response = discord.Embed(title='❗ No user targeted.')
    await message.channel.send(embed=response)
