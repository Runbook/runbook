"""Nexmo SMS Notification Reaction"""

import requests
import time

NEXMO_URL_TEMPLATE = 'https://rest.nexmo.com/sms/json?api_key={api_key}&api_secret={api_secret}&from={from_address}&to={to_address}&text={text}'


def __action(**kwargs):
    redata = kwargs['redata']
    jdata = kwargs['jdata']
    run = (
        jdata['failcount'] >= redata['trigger'] and
        (time.time() - float(redata['lastrun'])) >= redata['frequency'] and
        redata['data']['call_on'] in jdata['check']['status']
    )
    if run:
        api_key = redata['data']['api_key']
        api_secret = redata['data']['api_secret']
        from_address = redata['data']['from_address']
        to_address = redata['data']['to_address']
        text = redata['data']['text']
        return call_nexmo(api_key, api_secret, from_address, to_address, text)


def call_nexmo(api_key, api_secret, from_address, to_address, text):
    url = NEXMO_URL_TEMPLATE.format(
        api_key=api_key, api_secret=api_secret, from_address=from_address,
        to_address=to_address, text=text)
    r = requests.get(url).json()
    status = int(r[u'messages'][0][u'status'])
    assert not status, r[u'messages'][0][u'error-text']
    return True


def action(**kwargs):
    try:
        return __action(**kwargs)
    except Exception, e:
        redata = kwargs['redata']
        logger = kwargs['logger']
        logger.warning('nexmo-sms-notification: Reaction {id} failed: {message}'.format(
            id=redata['id'], message=e.message))
        return False
