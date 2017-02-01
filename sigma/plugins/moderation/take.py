from config import permitted_id
from sigma.core.permission import check_admin
import discord


async def take(cmd, message, args):
    if message.server:
        if message.author.id in permitted_id or check_admin(message.author, message.channel):
            if message.mentions:
                target = message.mentions[0]
                if target.bot:
                    out = discord.Embed(title=':exclamation: Can\'t award bots.', color=0xDB0000)
                    await cmd.bot.send_message(message.channel, None, embed=out)
                    return
                try:
                    amount = abs(int(args[0]))
                except:
                    out = discord.Embed(title=':exclamation: Invalid Input.', color=0xDB0000)
                    await cmd.bot.send_message(message.channel, None, embed=out)
                    return
                current_points = cmd.db.get_points(message.server, target)
                if current_points < amount:
                    out = discord.Embed(title=':exclamation: They don\'t have that many points.', color=0xDB0000)
                    await cmd.bot.send_message(message.channel, None, embed=out)
                    return
                cmd.db.take_points(message.server, target, amount)
                out = discord.Embed(title=':white_check_mark: Done', color=0x66CC66)
                out.add_field(name='Taken From', value=target.name + '#' + target.discriminator)
                out.add_field(name='Amount', value=str(amount))
                await cmd.bot.send_message(message.channel, None, embed=out)
                try:
                    out = discord.Embed(title=':fire: Points Were Taken Away', color=0xFF9900)
                    out.add_field(name='Server', value=message.server.name)
                    out.add_field(name='By', value=message.author.name + '#' + message.author.discriminator)
                    out.add_field(name='Amount', value=str(amount))
                    await cmd.bot.send_message(target, None, embed=out)
                except:
                    pass
            else:
                await cmd.bot.send_message(message.channel, cmd.help())
        else:
            status = discord.Embed(type='rich', color=0xDB0000,
                                   title=':no_entry: Insufficient Permissions. Bot Owner or Server Admin Only.')
            await cmd.bot.send_message(message.channel, None, embed=status)
