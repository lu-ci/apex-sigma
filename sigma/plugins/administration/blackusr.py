import discord


async def blackusr(cmd, message, args):
    if args:
        usr = discord.utils.find(lambda x: x.id == int(args[0]), cmd.bot.get_all_members())
        if usr:
            usr_black = cmd.db.find_one('BlacklistedUsers', {'UserID': usr.id})
            if usr_black:
                cmd.db.delete_one('BlacklistedUsers', {'UserID': usr.id})
                res_title = f'🔓 {usr.name}#{usr.discriminator} has been unblacklisted.'
            else:
                cmd.db.insert_one('BlacklistedUsers', {'UserID': usr.id})
                res_title = f'🔒 {usr.name}#{usr.discriminator} has been blacklisted.'
            response = discord.Embed(color=0xFF9900, title=res_title)
        else:
            response = discord.Embed(color=0xDB0000, title='❗ User not found!')
    else:
        response = discord.Embed(color=0xDB0000, title='❗ Nothing inputted!')
    await message.channel.send(embed=response)
