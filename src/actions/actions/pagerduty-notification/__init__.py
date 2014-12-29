#!/usr/bin/python
######################################################################
# Cloud Routes Bridge
# -------------------------------------------------------------------
# Actions Module
######################################################################

import syslog
import time

import pygerduty


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
        return actionPDTrigger(redata, jdata)
    else:
        return None


def actionPDTrigger(redata, jdata):
    ''' Perform EC2 Actions '''
    try:
        pager = pygerduty.PagerDuty(
            redata['data']['subdomain'],
            redata['data']['api_key'])
        try:
            service_key=redata['data']['service_key']
            description=redata['data']['description']
            details=redata['data']['details']
            incident_key=redata['data']['incident_key']

            # Should I test if incident_key is empty string or null?

            new_incident_key=pager.trigger_incident(service_key, description, incident_key, details)

            # What do I do with new_incident_key?

            return True
        except:
            return False
    except:
        line = "pagerduty-notification: Could not connect to PagerDuty for monitor %s" % jdata['cid']
        syslog.syslog(syslog.LOG_INFO, line)
        return False
