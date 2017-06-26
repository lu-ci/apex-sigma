import arrow
import discord
from .bandcamp_parser import parse_bandcamp_album


async def queuebandcamp(cmd, message, args):
    if args:
        qry = ' '.join(args)
        if 'bandcamp' in qry:
            initial_response = discord.Embed(color=0xFFCC66, title='💽 Processing...')
            init_resp_msg = await message.channel.send(embed=initial_response)
            songlist = await parse_bandcamp_album(qry)
            detection_response = discord.Embed(color=0xFFCC66, title=f'💽 Importing {len(songlist)} songs...')
            await init_resp_msg.edit(embed=detection_response)
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
            finished_response = discord.Embed(color=0xFFCC66, title=f'💽 Done! {len(songlist)} songs were imported!')
            await init_resp_msg.edit(embed=finished_response)
        else:
            no_qry_resp = discord.Embed(color=0xDB0000, title='❗ Not a BandCamp URL.')
            await message.channel.send(embed=no_qry_resp)
    else:
        no_qry_resp = discord.Embed(color=0xDB0000, title='❗ Nothing Inputted')
        await message.channel.send(embed=no_qry_resp)
