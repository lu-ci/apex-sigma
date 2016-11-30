import asyncio


async def inrole(cmd, message, args):
    if not args:
        await cmd.bot.send_message(message.channel, cmd.help())
        return
    else:
        role_input = ' '.join(args)
        out_text = ''
        role_choice = None
        for role in message.server.roles:
            if role.name.lower() == role_input.lower():
                role_choice = role
        if not role_choice:
            response = await cmd.bot.send_message(message.channel, 'No role by the name ' + role_input + ' was found.')
            await asyncio.sleep(10)
            await cmd.bot.delete_message(response)
            return
        else:
            out_text += 'The following users are in **' + role_choice.name + '**.\n\n'
            for member in message.server.members:
                for role in member.roles:
                    if role == role_choice:
                        out_text += member.name + ', '

            await cmd.bot.send_message(message.channel, out_text[:-2])
