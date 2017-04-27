from os import getenv, path

# This always points to the directory of the application
# Where the config.py file is located, don't touch it unless you know what you're doing
AppRoot = path.abspath(path.dirname(__file__))

# Bot Token
Token = getenv('DiscordBotToken') or ''
# API Keys
MongoAddress = getenv('MongoAddress') or '127.0.0.1'
MongoPort = getenv('MongoPort') or 27017
MongoAuth = getenv('MongoAuth') or False
MongoUser = getenv('MongoUser') or ''
MongoPass = getenv('MongoPass') or ''
DevMode = getenv('DevMode') or True
PlayingStatusRotation = getenv('PlayingStatusRotation') or False
DiscordListToken = getenv('DiscordListToken') or ''
DarkSkySecretKey = getenv('DarkSkySecretKey') or ''
MashapeKey = getenv('MashapeKey') or ''
RiotAPIKey = getenv('RiotAPIKey') or ''
CleverBotAPIKey = getenv('CleverBotAPIKey') or ''
GoogleAPIKey = getenv('GoogleAPIKey') or ''
GoogleCSECX = getenv('GoogleCSECX') or ''
OxfordDictKey = getenv('OxfordDictKey') or ''
OxfordDictClientID = getenv('OxfordDictClientID') or ''
WolframAlphaAppID = getenv('WolframAlphaAppID') or ''
RedditClientID = getenv('RedditClientID') or ''
RedditClientSecret = getenv('RedditClientSecret') or ''
HiRezDevID = getenv('HiRezDevID') or ''
HiRezAuthKey = getenv('HiRezAuthKey') or ''
LastFMAPIKey = getenv('LastFMAPIKey') or ''
ITADKey = getenv('ITADKey') or ''
SteamAPI = getenv('SteamAPI') or ''
SonarrKey = getenv('SonarrKey') or ''
BlizzardKey = getenv('BlizzardKey') or ''
RLAPIKey = getenv('RLAPIKey') or ''
ImgurClientID = getenv('ImgurClientID') or ''
ImgurClientSecret = getenv('ImgurClientSecret') or ''
WarGamingAppID = getenv('WarGamingAppID') or ''
TwitchClientID = getenv('TwitchClientID') or ''
OSUAPIKey = getenv('OSUAPIKey') or ''
Food2ForkAPIKey = getenv('Food2ForkAPIKey') or ''
CatAPIKey = getenv('CatAPIKey') or ''
TwitterConsumerKey = getenv('TwitterConsumerKey') or ''
TwitterSecret = getenv('TwitterSecret') or ''
TwitterToken = getenv('TwitterToken') or ''
TwitterTokenSecret = getenv('TwitterTokenSecret') or ''
ParagonAPIKey = getenv('ParagonAPIKey') or ''
SoundCloudClientID = getenv('SoundCloudClientID') or ''
MALUserName = getenv('MALUserName') or ''
MALPassword = getenv('MALPassword') or ''
# Bot Control Settings
MainServerURL = getenv('MainServerURL') or 'http://localhost/'
UseCachet = False
CachetToken = getenv('CachetToken') or ''
CachetURL = getenv('CachetURL') or ''
Prefix = '>>'
Currency = 'Kud ⚜'
SlotWinChannelID = 12345679123456789
permitted_id = [123456789123456789]
DefaultVolume = 100
