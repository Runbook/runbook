#!/usr/bin/python
######################################################################
# Cloud Routes Availability Manager: digitalocean-snapshot
# ------------------------------------------------------------------
# This module will query Digital Ocean's api and return all actions
# This will return true if there has been a "snapshot" in the last 30 minutes
# ------------------------------------------------------------------
# Author: Benjamin J. Cane - madflojo@cloudrout.es
######################################################################


import requests
import syslog
import datetime


def check(**kwargs):
    """ Checks Digital Ocean's api status for all actions"""
    jdata = kwargs['jdata']
    headers = {'Authorization': 'Bearer ' + jdata['data']['apikey'],
               'Content-Type': 'application/json'}
    url = "https://api.digitalocean.com/v2/actions"
    try:
        req = requests.get(url, timeout=3.0, headers=headers, verify=True)
    except:
        return False
    # parse JSON response, grabbing all actions
    all_actions = req.json()['actions']
    current_time = datetime.datetime.now()
    if req.status_code >= 200 and req.status_code < 300:
        line = "digitalocean-snapshot: Reqeust to {0} \
               sent for monitor {1} - Successful".format(url, jdata['cid'])
        syslog.syslog(syslog.LOG_INFO, line)
        # loop through all actions
        for action in all_actions:
            time_difference = current_time - datetime.datetime.strptime(
                action['completed_at'], '%Y-%m-%dT%H:%M:%SZ')
            # return True if action is a snapshot
            # and completed within the last 30 minutes
            if action['type'] == 'snapshot' and \
                    action['status'] == 'completed' \
                    and time_difference <= datetime.timedelta(minutes=30) \
                    and action['resource_id'] == jdata['data']['dropletid']:
                return True
            else:
                return False
    else:
        line = "digitalocean-snapshot: Request to {0} \
               sent for monitor {1} - False".format(url, jdata['cid'])
        syslog.syslog(syslog.LOG_INFO, line)
        return False
