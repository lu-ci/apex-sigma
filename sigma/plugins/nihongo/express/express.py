async def express(cmd, message, args):
    if args:
        try:
            express_q = int(args[0])
        except Exception as e:
            await cmd.reply('Must be a number.')
            return
        table = ['ちっとも （neg）',
                 '全く　（まったく） （neg）',
                 '全然　（ぜんぜん） （neg）',
                 'あまり （neg）',
                 'ほとんど （neg）',
                 'いまいち （neg）',
                 '特に　（とくに） （neg）',
                 '大して　（たいして） （neg）',
                 'ほんの少し　（ほんのすこし）',
                 'ほんのちょっと',
                 'やや',
                 '少し　（すこし）',
                 'ちょっと',
                 '些か　（いささか）',
                 '若干　（じゃっかん）',
                 '多少　（たしょう）',
                 'ある程度　（あるていど）',
                 'そこそこ',
                 'まあまあ',
                 'それなりに',
                 '割と　（わりと）',
                 '割かし　（わりかし）',
                 '大分　（だいぶ）',
                 '結構　（けっこう）',
                 '随分　（だいぶん）',
                 'とても',
                 'かなり',
                 '相当　（そうとう）',
                 '一際　（ひときわ）',
                 'とっても',
                 '大変　（たいへん）',
                 'やけに',
                 'やたら',
                 '凄く　（すごく）',
                 '非常に　（ひじょうに）',
                 '至って　（いたって）',
                 '極　（ごく）',
                 'チョー',
                 'めっちゃ',
                 'めちゃくちゃ',
                 '甚だしく　（はなはだしく）',
                 '極めて　（きわめて）',
                 '酷く　（ひどく）',
                 '思いっきり　（おもいっきり）',
                 'ものすごく',
                 'あまりにも',
                 'とてつもなく']
        if express_q < 0:
            express_q = 0
        if express_q > 100:
            express_q = 100
        result = table[int(express_q / 100 * (len(table) - 1))]
        await cmd.bot.send_message(message.channel, result)
    else:
        await cmd.bot.send_message(message.channel, cmd.help())
        return

