from config import permitted_id
import discord
import yaml


async def addreact(cmd, message, args):
    if args:
        with open(cmd.resource('responses.yml')) as response_file:
            data = yaml.safe_load(response_file)
        react_name = args[0].lower()
        react_url = ' '.join(args[1:])
        while react_url.endswith(' '):
            react_url = react_url[:-1]
        while react_url.startswith(' '):
            react_url = react_url[1:]
        if react_url.endswith('.gif'):
            if react_name in data:
                resp_list = data[react_name]
            else:
                resp_list = []
            if react_url not in resp_list:
                resp_data = {
                    'auth': message.author.name,
                    'url': react_url,
                    'srv': message.guild.name,
                    'sid': message.guild.id
                }
                resp_list.append(resp_data)
                data.update({react_name: resp_list})
                with open(cmd.resource('responses.yml'), 'w') as response_file:
                    yaml.safe_dump(data, response_file, default_flow_style=False)
                title = f'✅ {react_name.title()} response added.'
                color = 0x66CC66
            else:
                title = f'❗ Already in the list.'
                color = 0xDB0000
        else:
            title = f'❗ The link needs to be to a `.gif` directly.'
            color = 0xDB0000
        await message.channel.send(embed=discord.Embed(color=color, title=title))
