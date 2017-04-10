from config import permitted_id
import discord


async def leave(cmd, message, args):
    if message.author.id in permitted_id:
        if not args:
            await message.channel.send(cmd.help())
        else:
            search_id = args[0]
            try:
                for server in cmd.bot.guilds:
                    if server.id == int(search_id):
                        s_name = server.name
                        await cmd.bot.leave_server(server)
                        out = discord.Embed(title=':outbox_tray: I have left ' + s_name, color=0x66CC66)
                        await message.channel.send(None, embed=out)
                        return
                out = discord.Embed(title='❗ No server with that ID found.', color=0xDB0000)
                await message.channel.send(None, embed=out)
            except Exception as e:
                cmd.log.error(e)
    else:
        out = discord.Embed(type='rich', color=0xDB0000,
                            title='⛔ Insufficient Permissions. Bot Owner Only.')
        await message.channel.send(None, embed=out)
