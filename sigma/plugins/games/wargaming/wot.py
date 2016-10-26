from requests import get as rg

from config import WarGamingAppID


async def wot(cmd, message, args):
    q = ' '.join(args).lower()

    try:
        game_region, game_username = q.split(maxsplit=2)
    except:
        await cmd.reply('Insufficient parameters.')
        return

    regions_allowed = ['eu', 'na', 'asia', 'ru']

    if game_region not in regions_allowed:
        await cmd.reply(
                                       'Invalid region.\nThe bot only accepts `eu`, `na`, `ru` and `asia`')
        return

    if game_region == 'na':
        game_region = 'com'

    try:
        url_base = ('https://api.worldoftanks.' + game_region + '/wot/account/list/?application_id=' + WarGamingAppID + '&search=' + game_username)
        initial_data = rg(url_base).json()
    except:
        await cmd.reply('`' + game_region + '` is not a valid region.')
        return

    try:
        if initial_data['status'].lower() == 'ok':
            pass
        else:
            return
    except Exception as e:
        cmd.log.error(e)
        return

    try:
        game_nickname = initial_data['data'][0]['nickname']
    except:
        await cmd.reply('User `' + game_username + '` not found.')
        return

    account_id = initial_data['data'][0]['account_id']
    url_second = 'https://api.worldofwarships.' + game_region + '/wows/account/info/?application_id=' + WarGamingAppID + '&account_id=' + str(account_id)
    main_data = rg(url_second).json()

    try:
        if main_data['status'].lower() == 'ok':
            pass
        else:
            return
    except Exception as e:
        cmd.log.error(e)
        return

    try:
        data = main_data['data'][str(account_id)]
        stats = data['statistics']['all']
        spotted = stats['spotted']
        max_xp = stats['max_xp']

        # Divider for clarity

        out_text = '```haskell'

        out_text += '\n```'

        # Divider for clarity

        await cmd.reply(out_text)
    except SyntaxError as e:
        cmd.log.error(e)
        await cmd.reply('We ran into an error, the user most likely doesn\'t exist in the region, or something dun goofed.\nError: **' + str(e) + '**')
        return
