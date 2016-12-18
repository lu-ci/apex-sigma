from config import permitted_id
import asyncio
import discord


async def announce(cmd, message, args):
    if message.author.id in permitted_id:
        if not args:
            out_content = discord.Embed(type='rich', color=0xDB0000,
                                        title=':no_entry: Insufficient Permissions. Bot Owner Only.')
            await cmd.bot.send_message(message.channel, None, embed=out_content)
            return
        else:
            success = 0
            failed = 0
            announcement = ' '.join(args)
            for server in cmd.bot.servers:
                try:
                    announce_content = discord.Embed(type='rich', color=0x0099FF)
                    announce_content.add_field(name=':mega: Announcement', value=announcement)
                    announce_content.set_author(name=message.author.name, icon_url=message.author.avatar_url)
                    await cmd.bot.send_message(server.default_channel, None, embed=announce_content)
                    success += 1
                    cmd.log.info('Success on ' + server.name)
                except Exception as e:
                    failed += 1
                    cmd.log.info('Failed on ' + server.name + '\n' + str(e))
                    pass
                await asyncio.sleep(0.20)
            out_content = discord.Embed(type='rich', color=0x66cc66, title=':white_check_mark: Announcement Done')
            out_content.add_field(name='Success', value=str(success))
            out_content.add_field(name='Failed', value=str(failed))
            await cmd.bot.send_message(message.channel, None, embed=out_content)
