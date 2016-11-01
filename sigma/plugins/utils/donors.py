from sigma.core.formatting import bold
import yaml
from humanfriendly.tables import format_pretty_table

async def donors(cmd, message, args):
    with open('DONORS') as donors_file:
        content = yaml.load(donors_file)
        donors = content['donors']
    don_lst = []
    for don in donors:
        temp_lst = []
        temp_lst.append(don)
        don_lst.append(temp_lst)
    donor_list = format_pretty_table(don_lst)
    out_text = 'The lovely people that support the **Aurora Project**:'
    out_text += '```haskell'
    out_text += '\n' + donor_list
    out_text += '\n```'
    out_text += '\nPlease consider donating by following instructions on the Donor page.'
    out_text += '\n<https://auroraproject.xyz/donors>!'
    out_text += '\nThank you! :ribbon:'

    await cmd.reply(out_text)
