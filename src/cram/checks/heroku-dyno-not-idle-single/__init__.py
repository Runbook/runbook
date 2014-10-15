#!/usr/bin/python
######################################################################
# Cloud Routes Availability Manager: heroku-dyno-not-idle-single module
# ------------------------------------------------------------------
# This module will query Heroku's api and check for a single dyno's status
# This will return true if no errors or false if there are errors
# ------------------------------------------------------------------
# Author: Benjamin J. Cane - madflojo@cloudrout.es
######################################################################

import requests
import json
import base64
import syslog


def check(data):
    """ Checks Heroku's api status for a specified dyno """
    basekey = base64.b64encode(":" + data['data']['apikey'])
    headers = {
        "Accept": "application/vnd.heroku+json; version=3",
        "Authorization": basekey
    }
    timeout = 5.00
    url = "https://api.heroku.com/apps/" + \
        data['data']['appname'] + "/dynos/" + data['data']['dynoname']
    try:
        result = requests.get(
            url, timeout=timeout, headers=headers, verify=True)
    except:
        return None
    line = "heroku-dyno-status: Got response from heroku for monitor - %s" % (
        result.text)
    syslog.syslog(syslog.LOG_DEBUG, line)
    retdata = json.loads(result.text)
    if "state" in retdata:
        if retdata['state'] == "idle":
            return False
        else:
            return True
    else:
        return None
