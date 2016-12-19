from config import permitted_id
import discord


async def searchid(cmd, message, args):
    if message.author.id in permitted_id:
        if not args:
            cmd.bot.send_message(message.channel, cmd.help())
            return
        else:
            search_id = args[0]
        count = 0
        embed = discord.Embed(title=':information_source: User Found On The Following Servers', color=0x0099FF)
        for server in cmd.bot.servers:
            for user in server.members:
                if user.id == search_id:
                    count += 1
                    embed.add_field(name=server.name, value=server.id)
        if count == 0:
            embed = discord.Embed(title=':information_source: User Not Found', color=0x0099FF)
        await cmd.bot.send_message(message.channel, None, embed=embed)
    else:
        out = discord.Embed(type='rich', color=0xDB0000,
                            title=':no_entry: Insufficient Permissions. Bot Owner Only.')
        await cmd.bot.send_message(message.channel, None, embed=out)
