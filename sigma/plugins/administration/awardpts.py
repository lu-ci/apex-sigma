from config import permitted_id
from sigma.core.permission import check_admin
import discord


async def awardpts(cmd, message, args):
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
            cmd.db.add_points(message.server, target, amount)
            out = discord.Embed(title='✅ Done', color=0x66CC66)
            out.add_field(name='Sent To', value=target.name + '#' + target.discriminator)
            out.add_field(name='Amount', value=str(amount))
            await cmd.bot.send_message(message.channel, None, embed=out)
            try:
                out = discord.Embed(title=':gem: You Were Given Points', color=0x0099FF)
                out.add_field(name='Server', value=message.server.name)
                out.add_field(name='From', value=message.author.name + '#' + message.author.discriminator)
                out.add_field(name='Amount', value=str(amount))
                await cmd.bot.send_message(target, None, embed=out)
            except:
                pass
        else:
            await cmd.bot.send_message(message.channel, cmd.help())
    else:
        status = discord.Embed(type='rich', color=0xDB0000,
                               title='⛔ Insufficient Permissions. Bot Owner or Server Admin Only.')
        await cmd.bot.send_message(message.channel, None, embed=status)
