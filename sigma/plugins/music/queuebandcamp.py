import arrow
import discord
from .bandcamp_parser import parse_bandcamp_album


async def queuebandcamp(cmd, message, args):
    if args:
        qry = ' '.join(args)
        if qry.startswith('<'):
            qry = qry[1:]
        if qry.endswith('>'):
            qry = qry[:-1]
        if 'bandcamp' in qry:
            initial_response = discord.Embed(color=0xFFCC66, title='💽 Processing...')
            init_resp_msg = await message.channel.send(embed=initial_response)
            songlist = await parse_bandcamp_album(qry)
            for song in songlist:
                sound_type = 2
                data = {
                    'url': song['url'],
                    'type': sound_type,
                    'requester': message.author,
                    'sound': song,
                    'timestamp': arrow.now().timestamp
                }
                await cmd.bot.music.add_to_queue(message.guild.id, data)
            if len(songlist) > 1:
                finished_response = discord.Embed(color=0xFFCC66,
                                                  title=f'💽 Done! {len(songlist)} songs were imported!')
            else:
                resp_title = f'💽 Done! {songlist[0]["artist"]} - {songlist[0]["title"]} was imported!'
                finished_response = discord.Embed(color=0xFFCC66, title=resp_title)
            await init_resp_msg.edit(embed=finished_response)
        else:
            no_qry_resp = discord.Embed(color=0xDB0000, title='❗ Not a BandCamp URL.')
            await message.channel.send(embed=no_qry_resp)
    else:
        no_qry_resp = discord.Embed(color=0xDB0000, title='❗ Nothing Inputted')
        await message.channel.send(embed=no_qry_resp)
