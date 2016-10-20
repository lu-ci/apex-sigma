async def karaokestatus(cmd, message, args):
    out = 'Karaoke mode ' + bold(boolToStr(karaoke_mod)) + '\n'
    out += 'Session ongoing ' + bold(boolToStr(karaoke)) + '\n'
    out += 'Channel ' + bold(karaoke_channel) + '\n'
    out += 'Strict mode ' + bold(boolToStr(karaoke_strict))

    await cmd.reply(out)
