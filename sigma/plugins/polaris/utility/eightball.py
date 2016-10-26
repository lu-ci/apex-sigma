import random
import yaml


async def eightball(cmd, message, args):
    if args:
        question = ' '.join(args)
        with open(cmd.resource('eb_answers.yml')) as eball_file:
            content = yaml.load(eball_file)
            answers = content['answers']
            answer = random.choice(answers)
            out_text = '**Question**: `' + question + '`'
            out_text += '\n**Answer**: `' + answer + '`'
            await cmd.reply(out_text)
    else:
        await cmd.reply(cmd.help())
        return
