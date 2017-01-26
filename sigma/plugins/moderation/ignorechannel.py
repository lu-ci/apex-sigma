import discord
from sigma.core.permission import check_admin


async def ignorechannel(cmd, message, args):
    if check_admin(message.author, message.channel):
        target = None
        if not args:
            await cmd.bot.send_message(message.channel, cmd.help())
            return
        qry = ' '.join(args)
        if qry.startswith('<#'):
            search_id = qry.replace('<#', '').replace('>', '')
        else:
            search_id = args[0]
        for chan in message.server.channels:
            if chan.id == search_id:
                target = chan
                break
        if not target:
            embed = discord.Embed(color=0x696969, title=':notebook: No channel like that was found on this server.')
        else:
            if target == message.author:
                embed = discord.Embed(title=':warning: You Can\'t Blacklist Yourself', color=0xFF9900)
                await cmd.bot.send_message(message.channel, None, embed=embed)
                return
            if target == cmd.bot.user:
                embed = discord.Embed(title=':warning: You Can\'t Blacklist Me', color=0xFF9900)
                await cmd.bot.send_message(message.channel, None, embed=embed)
                return
            black = cmd.db.get_settings(message.server.id, 'BlacklistedChannels')
            if not black:
                black = []
            if target.id in black:
                black.remove(target.id)
                embed = discord.Embed(title=':unlock: ' + target.name + 'has been un-blacklisted.', color=0xFF9900)
            else:
                black.append(target.id)
                embed = discord.Embed(title=':lock: ' + target.name + 'has been blacklisted.', color=0xFF9900)
            cmd.db.set_settings(message.server.id, 'BlacklistedChannels', black)
    else:
        embed = discord.Embed(type='rich', color=0xDB0000,
                              title=':no_entry: Insufficient Permissions. Server Admin Only.')
    await cmd.bot.send_message(message.channel, None, embed=embed)
