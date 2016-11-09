async def invite(cmd, message, args):
    out_txt = 'To invite me to a Discord server, click this link:'
    out_txt += '\nhttps://discordapp.com/oauth2/authorize?client_id=' + cmd.bot.user.id + '&scope=bot&permissions=66186303'
    await cmd.bot.send_message(message.channel, out_txt)
