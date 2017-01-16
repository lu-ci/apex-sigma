import random
import yaml
import discord


async def eightball(cmd, message, args):
    if args:
        question = ' '.join(args)
        with open(cmd.resource('eb_answers.yml')) as eball_file:
            content = yaml.load(eball_file)
            answers = content['answers']
            answer = random.choice(answers)
            embed = discord.Embed(color=0x1abc9c, title='🎱 You Gaze Into The Magic 8Ball')
            embed.add_field(name='Question', value='```\n' + question + '\n```', inline=True)
            embed.add_field(name='Answer', value='```\n' + answer + '\n```', inline=True)
            await cmd.bot.send_message(message.channel, None, embed=embed)
    else:
        await cmd.bot.send_message(message.channel, cmd.help())
        return
