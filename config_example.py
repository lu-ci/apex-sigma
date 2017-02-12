from os import getenv, path

# This always points to the directory of the application
# where the config.py file is located
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
DiscordListToken = getenv('DiscordListToken') or ''
GitHubWebserverPort = getenv('GitHubWebserverPort') or 8080
GitHubWebserverAddr = getenv('GitHubWebserverAddr') or 'localhost'
DarkSkySecretKey = getenv('DarkSkySecretKey') or ''
MashapeKey = getenv('MashapeKey') or ''
RiotAPIKey = getenv('RiotAPIKey') or ''
CleverBotAPIKey = getenv('CleverBotAPIKey') or ''
GoogleAPIKey = getenv('GoogleAPIKey') or ''
GoogleAuthFileLocation = getenv('GoogleAuthFileLocation') or ''
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
mal_un = getenv('mal_un') or ''
mal_pw = getenv('mal_pw') or ''
# Bot Control Settings
MainServerURL = getenv('MainServerURL') or 'http://localhost/'
Prefix = '>>'
permitted_id = ['123456789123456789']
