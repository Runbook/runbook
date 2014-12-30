"""Twilio SMS Notification Reaction"""

import time
from twilio.rest import TwilioRestClient


def __action(**kwargs):
    redata = kwargs['redata']
    jdata = kwargs['jdata']
    run = (
        jdata['failcount'] >= redata['trigger'] and
        (time.time() - float(redata['lastrun'])) >= redata['frequency'] and
        redata['data']['call_on'] in jdata['check']['status']
    )
    if run:
        account_sid = redata['data']['account_sid']
        auth_token = redata['data']['auth_token']
        from_address = redata['data']['from_address']
        to_address = redata['data']['to_address']
        text = redata['data']['text']
        return call_twilio(account_sid, auth_token, from_address, to_address, text)


def call_twilio(account_sid, auth_token, from_address, to_address, text):
    client = TwilioRestClient(account_sid, auth_token)
    message = client.messages.create(to=to_address,from_=from_address,body=text)
    assert message.status not in ('failed', 'undelivered'), message.ErrorMessage
    return True


def action(**kwargs):
    try:
        return __action(**kwargs)
    except Exception, e:
        redata = kwargs['redata']
        logger = kwargs['logger']
        logger.warning('twilio-sms-notification: Reaction {id} failed: {message}'.format(
            id=redata['id'], message=e.message))
        return False
