from sigma.core.permission import check_ban
import discord


async def unban(cmd, message, args):
    if not check_ban(message.author, message.channel):
        response = discord.Embed(title='⛔ Unpermitted. Ban Permissions Needed.', color=0xDB0000)
    else:
        if args:
            user_search = ' '.join(args)
            target = None
            banlist = await message.guild.bans()
            for entry in banlist:
                if entry.user.name.lower() == user_search.lower():
                    target = entry.user
                    break
            if target:
                await message.guild.unban(target,
                                          reason=f'Unbanned by {message.author.name}#{message.author.discriminator}.')
                response = discord.Embed(title=f'✅ {target.name} has been unbanned.', color=0x66CC66)
            else:
                response = discord.Embed(title=f'🔍 {user_search} not found in the ban list.')
        else:
            response = discord.Embed(title='❗ No user targeted.', color=0xDB0000)
    await message.channel.send(embed=response)
