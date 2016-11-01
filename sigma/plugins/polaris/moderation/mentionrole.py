import asyncio
from sigma.core.permission import check_admin


async def mentionrole(cmd, message, args):
    if not args:
        await cmd.reply(cmd.help())
        return
    else:
        if check_admin(message.author, message.channel):
            role_input = ' '.join(args)
            out_text = ''
            role_choice = None
            for role in message.server.roles:
                if role.name.lower() == role_input.lower():
                    role_choice = role
            if not role_choice:
                response = await cmd.reply('No role by the name ' + role_input + ' was found.')
                await asyncio.sleep(10)
                await cmd.bot.delete_message(response)
                return
            else:
                out_text += 'User <@' + message.author.id + '> has invoked a role mention for the role **' + role_choice.name + '**.\n\n'
                for member in message.server.members:
                    for role in member.roles:
                        if role == role_choice:
                            out_text += '<@' + member.id + '>, '

                await cmd.reply(out_text[:-2])
        else:
            response = await cmd.reply(
                'Only a user with the **Manage Messages and Manage Roles** privilege can use this command. :x:')
            await asyncio.sleep(10)
            await cmd.bot.delete_message(response)
