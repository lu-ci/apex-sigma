from os import getenv

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
mal_un = getenv('mal_un') or ''
mal_pw = getenv('mal_pw') or ''
# Bot Control Settings
MainServerURL = getenv('MainServerURL') or 'localhost'
Prefix = '>>'
permitted_id = ['123456789123456789']
