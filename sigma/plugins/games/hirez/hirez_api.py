import hashlib
import arrow
import json
import aiohttp
from config import HiRezAuthKey, HiRezDevID

api_session = {
    'SessionID': None,
    'GeneratedStamp': 0
}
smite_base_url = 'http://api.smitegame.com/smiteapi.svc/'
paladins_base_url = 'http://api.paladins.com/paladinsapi.svc/'


def make_timestamp():
    utc = arrow.utcnow()
    hr_ts = utc.format('YYYYMMDDHHmmss')
    return hr_ts


def make_signature(session_name):
    timestamp = make_timestamp()
    qry = HiRezDevID + session_name + HiRezAuthKey + timestamp
    crypt = hashlib.new('md5')
    crypt.update(qry.encode('utf-8'))
    final = crypt.hexdigest()
    return final


async def new_session():
    timestamp = make_timestamp()
    genstamp = arrow.utcnow().timestamp
    signature = make_signature('createsession')
    access_url = smite_base_url + 'createsessionJson/' + HiRezDevID + '/' + signature + '/' + timestamp
    async with aiohttp.ClientSession() as session:
        async with session.get(access_url) as data:
            data = await data.read()
            data = json.loads(data)
    session_id = data['session_id']
    api_session.update({
        'SessionID': session_id,
        'GeneratedStamp': genstamp
    })
    return


async def get_session():
    curr_stamp = arrow.utcnow().timestamp
    if not api_session['SessionID'] or (api_session['GeneratedStamp'] + 980) < curr_stamp:
        await new_session()
        session_id = api_session['SessionID']
    else:
        session_id = api_session['SessionID']
    return session_id
