from config import permitted_id
import discord


async def searchid(cmd, message, args):
    if message.author.id in permitted_id:
        if not args:
            cmd.bot.send_message(message.channel, cmd.help())
            return
        else:
            search_id = int(args[0])
        count = 0
        embed = discord.Embed(title='ℹ User Found On The Following Servers', color=0x0099FF)
        for server in cmd.bot.guilds:
            for user in server.members:
                if user.id == search_id:
                    count += 1
                    embed.add_field(name=server.name, value=server.id)
        if count == 0:
            embed = discord.Embed(title='ℹ User Not Found', color=0x0099FF)
        await message.channel.send(None, embed=embed)
    else:
        out = discord.Embed(type='rich', color=0xDB0000,
                            title='⛔ Insufficient Permissions. Bot Owner Only.')
        await message.channel.send(None, embed=out)
