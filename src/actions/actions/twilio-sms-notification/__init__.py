"""Twilio SMS Notification Reaction"""

import time
from twilio.rest import TwilioRestClient
from .. import BaseReaction


class Reaction(BaseReaction):

    def _Action(self):
        account_sid = self.redata['data']['account_sid']
        auth_token = self.redata['data']['auth_token']
        from_address = self.redata['data']['from_address']
        to_address = self.redata['data']['to_address']
        text = self.redata['data']['text']
        client = TwilioRestClient(account_sid, auth_token)
        message = client.messages.create(
            to=to_address,
            from_=from_address,
            body=text)
        assert message.status not in ('failed', 'undelivered'), \
            message.ErrorMessage
        return True
