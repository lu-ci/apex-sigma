from sigma.core.permission import check_ban
import discord


async def softban(cmd, message, args):
    if not check_ban(message.author, message.channel):
        response = discord.Embed(title='⛔ Unpermitted. Ban Permissions Needed.', color=0xDB0000)
    else:
        if message.mentions:
            target = message.mentions[0]
            if target.id == message.author.id:
                response = discord.Embed(title='⛔ You can\'t soft-ban yourself.', color=0xDB0000)
            else:
                await target.ban(reason=f'Soft-banned by {message.author.name}#{message.author.discriminator}.')
                await target.unban(reason=f'Soft-banned by {message.author.name}#{message.author.discriminator}.')
                response = discord.Embed(title=f'🔨 {target.name} has been soft-banned.')
        else:
            response = discord.Embed(title='❗ No user targeted.')
    await message.channel.send(embed=response)
