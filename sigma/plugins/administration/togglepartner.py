import discord


async def togglepartner(cmd, message, args):
    if args:
        target_sid = int(args[0])
        target_server = discord.utils.find(lambda x: x.id == target_sid, cmd.bot.guilds)
        if target_server:
            try:
                partner = cmd.db.get_settings(target_sid, 'IsPartner')
            except:
                cmd.db.set_settings(target_sid, 'IsPartner', False)
                partner = False
            if partner:
                cmd.db.set_settings(target_sid, 'IsPartner', False)
                response = discord.Embed(color=0xFF9900, title=f'🔥 {target_server.name} is no longer a partner.')
            else:
                cmd.db.set_settings(target_sid, 'IsPartner', True)
                response = discord.Embed(color=0x0099FF, title=f'💎 {target_server.name} has been made a partner.')
        else:
            response = discord.Embed(color=0x696969, title='🔍 Not Server With That ID Was Found')
        await message.channel.send(None, embed=response)
