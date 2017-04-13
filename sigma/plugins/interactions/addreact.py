from config import permitted_id
import discord
import yaml


async def addreact(cmd, message, args):
    if message.guild.id == 287978175927943188 or message.author.id in permitted_id:
        if args:
            with open(cmd.resource('responses.yml')) as response_file:
                data = yaml.safe_load(response_file)
            react_name = args[0].lower()
            react_url = ' '.join(args[1:])
            if react_name in data:
                resp_list = data[react_name]
            else:
                resp_list = []
            if react_url not in resp_list:
                resp_list.append(react_url)
                data.update({react_name: resp_list})
                with open(cmd.resource('responses.yml'), 'w') as response_file:
                    yaml.safe_dump(data, response_file, default_flow_style=False)
                title = f'✅ {react_name.title()} response added.'
            else:
                title = f'❗ Already in the list.'
            await message.channel.send(embed=discord.Embed(color=0x1ABC9C, title=title))
