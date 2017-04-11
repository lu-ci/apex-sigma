import discord


async def invite(cmd, message, args):
    embed = discord.Embed(title='ℹ Click here to invite me to your Discord server.', color=0x0099FF,
                          url=f'\nhttps://discordapp.com/oauth2/authorize?client_id={cmd.bot.user.id}&scope=bot&permissions=8')
    await message.channel.send(None, embed=embed)
