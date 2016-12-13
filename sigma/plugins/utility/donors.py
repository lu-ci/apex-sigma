import yaml
from humanfriendly.tables import format_pretty_table

async def donors(cmd, message, args):
    with open('DONORS') as donors_file:
        content = yaml.load(donors_file)
        donors = content['donors']
    don_lst = []
    for don in donors:
        temp_lst = [don['name']]
        don_lst.append(temp_lst)
    donor_list = format_pretty_table(don_lst)
    out_text = 'The lovely people that support the **Aurora Project**:'
    out_text += '```haskell'
    out_text += '\n' + donor_list
    out_text += '\n```'
    out_text += '\nPlease consider donating by visiting the paypal.me page here:'
    out_text += '\n<https://www.paypal.me/AleksaRadovic>'
    out_text += '\nThe current donors can be seen here!'
    out_text += '\n<https://auroraproject.xyz#donors>!'
    out_text += '\nThank you! :ribbon:'

    await cmd.bot.send_message(message.channel, out_text)
