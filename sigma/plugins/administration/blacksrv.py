from config import permitted_id
import discord


async def blacksrv(cmd, message, args):
    if message.author.id in permitted_id:
        if not args:
            await message.channel.send(cmd.help())
            return
        target = None
        for server in cmd.bot.guilds:
            if server.id == args[0]:
                target = server
                break
        if target:
            black = cmd.db.get_settings(target.id, 'IsBlacklisted')
            if black:
                cmd.db.set_settings(target.id, 'IsBlacklisted', False)
                embed = discord.Embed(title=':unlock: Server ' + target.name + ' has been un-blacklisted.',
                                      color=0xFF9900)
            else:
                cmd.db.set_settings(target.id, 'IsBlacklisted', True)
                embed = discord.Embed(title=':lock: Server ' + target.name + ' has been blacklisted.', color=0xFF9900)
        else:
            embed = discord.Embed(type='rich', color=0xDB0000,
                                  title='❗ No server by that ID was found.')
        await message.channel.send(None, embed=embed)
    else:
        out_content = discord.Embed(type='rich', color=0xDB0000,
                                    title='⛔ Insufficient Permissions. Bot Owner Only.')
        await message.channel.send(None, embed=out_content)
