import discord
from sigma.core.permission import check_man_roles


async def wftag(cmd, message, args):
    if check_man_roles(message.author, message.channel):
        if args:
            if len(args) > 1:
                alert_tag = args[0].lower()
                alert_role_search = ' '.join(args[1:]).lower()
                alert_role = None
                for role in message.guild.roles:
                    if role.name.lower() == alert_role_search:
                        alert_role = role
                        break
                if alert_role:
                    try:
                        wf_tags = cmd.db.get_settings(message.guild.id, 'WarframeTags')
                    except:
                        wf_tags = {}
                    if alert_tag not in wf_tags:
                        response_title = f'`{alert_tag.upper()}` has been bound to {alert_role.name}'
                    else:
                        response_title = f'`{alert_tag.upper()}` has been updated to bind to {alert_role.name}'
                    wf_tags.update({alert_tag: alert_role.id})
                    cmd.db.set_settings(message.guild.id, 'WarframeTags', wf_tags)
                    response = discord.Embed(title=f'✅ {response_title}', color=0x66CC66)
                else:
                    response = discord.Embed(title=f'❗ {alert_role_search.upper()} Was Not Found', color=0xDB0000)
            else:
                response = discord.Embed(title='❗ Not Enough Arguments', color=0xDB0000)
        else:
            response = discord.Embed(title='❗ Nothing Was Inputted', color=0xDB0000)
    else:
        response = discord.Embed(title='⛔ Unpermitted. Manage Roles Permission Required.', color=0xDB0000)
    await message.channel.send(embed=response)
