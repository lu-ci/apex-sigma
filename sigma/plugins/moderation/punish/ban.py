from sigma.core.permission import check_ban
import discord


async def ban(cmd, message, args):
    if not check_ban(message.author, message.channel):
        response = discord.Embed(title='⛔ Unpermitted. Ban Permissions Needed.', color=0xDB0000)
    else:
        if message.mentions:
            target = message.mentions[0]
            if target.id == message.author.id:
                response = discord.Embed(title='⛔ You can\'t kick yourself.', color=0xDB0000)
            else:
                await target.ban(reason=f'Banned by {message.author.name}#{message.author.discriminator}.')
                response = discord.Embed(title=f'🔨 {target.name} has been banned.')
        else:
            response = discord.Embed(title='❗ No user targeted.')
    await message.channel.send(embed=response)
