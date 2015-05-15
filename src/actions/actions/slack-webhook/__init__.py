"""Twilio SMS Notification Reaction"""

import time
import requests
import json
from .. import BaseReaction


class Reaction(BaseReaction):

    def _Action(self):
        payload = {
            'username' : 'Runbook',
            'text' : self.redata['data']['body'],
            'channel' : self.redata['data']['channel']
        }
        json_payload = json.dumps(payload)
        url = self.redata['data']['url']
        req = requests.post(
            url=url,
            data=json_payload,
            timeout=10,
            stream=True,
            verify=False)
        req.close()
        assert req.status_code is 200, "Error calling slack: %d" % req.status_code
        return True
