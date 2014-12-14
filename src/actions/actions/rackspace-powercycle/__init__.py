#!/usr/bin/python
######################################################################
# Cloud Routes Bridge
# -------------------------------------------------------------------
# Actions Module
######################################################################

import syslog
import requests
import json
import time



def action(**kwargs):
    ''' This method is called to action a reaction '''
    redata = kwargs['redata']
    jdata = kwargs['jdata']
    run = True
    # Check for Trigger
    if redata['trigger'] > jdata['failcount']:
        run = False

    # Check for lastrun
    checktime = time.time() - float(redata['lastrun'])
    if checktime < redata['frequency']:
        run = False

    if redata['data']['call_on'] not in jdata['check']['status']:
        run = False

    if run:
        return call_action(redata, jdata)
    else:
        return None

def call_action(redata, jdata):
    ''' Perform actual call '''

    # Authenticate with Rackspace ID service
    headers = {'Content-Type': 'application/json'}
    authmsg = {
        "auth": {
            "RAX-KSKEY:apiKeyCredentials": {
                "username": redata['data']['username'],
                "apiKey": redata['data']['apikey']
            }
        }
    }
    payload = json.dumps(authmsg)
    url = "https://identity.api.rackspacecloud.com/v2.0/tokens"
    try:
        req = requests.post(
            url, timeout=10.0, data=payload, headers=headers, verify=True)
        retdata = json.loads(req.text)
        # Check Status code and grab required fields from auth data
        if req.status_code == 200:
            token = retdata['access']['token']['id']
            for catalog in retdata['access']['serviceCatalog']:
                if catalog['name'] == redata['data']['resource_type']:
                    for endpoint in catalog['endpoints']:
                        if endpoint['region'] == redata['data']['region']:
                            url = endpoint['publicURL'] + "/servers/" + redata['data']['serverid'] + "/action"
            # Send Reboot Request
            headers = {
                "X-Auth-Token": token,
                "Content-Type": "application/json"
            }
            msg = {
                "reboot": {
                    "type": "HARD"
                }
            }
            payload = json.dumps(msg)
            try:
                req = requests.post(
                    url, timeout=10.0, data=payload,
                    headers=headers, verify=True)
            except:
                line = "rackspace-powercycle: False Rackspace API Call for reaction %s" % (redata['id'])
                syslog.syslog(syslog.LOG_INFO, line)
                return False
        else:
            line = "rackspace-powercycle: False Rackspace Authenticaiton for reaction %s" % (redata['id'])
            syslog.syslog(syslog.LOG_INFO, line)
            return False
    except:
        line = "rackspace-powercycle: False Rackspace Authenticaiton for reaction %s" % (redata['id'])
        syslog.syslog(syslog.LOG_INFO, line)
        return False
    if req.status_code == 202:
        line = "rackspace-powercycle: Reqeust to %s sent for monitor %s - Successful" % (url, jdata['cid'])
        syslog.syslog(syslog.LOG_INFO, line)
        return True
    else:
        line = "rackspace-powercycle: Request to %s sent for monitor %s - False" % (url, jdata['cid'])
        syslog.syslog(syslog.LOG_INFO, line)
        return False
