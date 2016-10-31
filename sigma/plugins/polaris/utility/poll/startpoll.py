import random


async def startpoll(cmd, message, args):
    if not args:
        await cmd.reply(cmd.help())
        return
    else:
        full_input = ' '.join(args)
        split_poll_args = full_input.split('; ')
        question = split_poll_args[0]
        answers = split_poll_args[1:]
        poll_id = random.randint(1000, 99999)

        answers_text = ''
        n = 0

        for answer in answers:
            n += 1
            answers_text += '\n#' + str(n) + ': ' + answer

        out_text = '```haskell'
        out_text += '\nQuestion: ' + question
        out_text += '\nID: ' + str(poll_id)
        out_text += '\n' + answers_text
        out_text += '\n```'

        await cmd.reply(out_text)

