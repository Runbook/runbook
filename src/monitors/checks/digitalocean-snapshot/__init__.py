#!/usr/bin/python
######################################################################
# Cloud Routes Availability Manager: digitalocean-snapshot
# ------------------------------------------------------------------
# This module will query Heroku's api and check for a single dyno's status
# This will return true if no errors or false if there are errors
# ------------------------------------------------------------------
# Author: Benjamin J. Cane - madflojo@cloudrout.es
######################################################################


import requests
import json
import syslog


def check(data):
    """ Checks Heroku's api status for dyno status"""
    headers = {'Authorization': 'Bearer ' + data['data']['apikey'],
               'Content-Type': 'application/json'}
    url = "https://api.digitalocean.com/v2/droplets/%s/actions" % str(
        data['data']['dropletid'])
    msg = {"type": "snapshot"}
    payload = json.dumps(msg)
    try:
        req = requests.post(
            url, timeout=3.0, data=payload, headers=headers, verify=True)
    except:
        return False
    if req.status_code >= 200 and req.status_code < 300:
        line = "digitalocean-snapshot: Reqeust to {0} \
               sent for monitor {1} - Successful".format(url, data['cid'])
        syslog.syslog(syslog.LOG_INFO, line)
        return True
    else:
        line = "digitalocean-snapshot: Request to {0} \
               sent for monitor {1} - False".format(url, data['cid'])
        syslog.syslog(syslog.LOG_INFO, line)
        return False
