import asyncio
import discord


async def announceglobal(cmd, message, args):
    if not args:
        out_content = discord.Embed(type='rich', color=0xDB0000, title='❗ Empty Message.')
        await message.channel.send(None, embed=out_content)
        return
    else:
        success = 0
        failed = 0
        disabled = 0
        announcement = ' '.join(args)
        for server in cmd.bot.guilds:
            ann = cmd.db.get_settings(server.id, 'Announcement')
            annch = cmd.db.get_settings(server.id, 'AnnouncementChannel')
            target_ch = discord.utils.find(lambda c: c.id == annch, server.channels)
            if ann:
                try:
                    announce_content = discord.Embed(type='rich', color=0x0099FF)
                    announce_content.add_field(name=':mega: Announcement', value=announcement)
                    announce_content.set_author(name=message.author.name, icon_url=message.author.avatar_url)
                    await target_ch.send(None, embed=announce_content)
                    success += 1
                    cmd.log.info('Success on ' + server.name)
                except Exception as e:
                    failed += 1
                    cmd.log.info('Failed on ' + server.name + '\n' + str(e))
                    pass
                await asyncio.sleep(0.05)
            else:
                cmd.log.info('Disabled on ' + server.name)
                disabled += 1
        out_content = discord.Embed(type='rich', color=0x66cc66, title='✅ Announcement Done')
        out_content.add_field(name='Success', value=str(success))
        out_content.add_field(name='Disabled', value=str(disabled))
        out_content.add_field(name='Failed', value=str(failed))
        await message.channel.send(None, embed=out_content)
