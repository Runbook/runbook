#!/usr/bin/python
######################################################################
# Cloud Routes Bridge
# -------------------------------------------------------------------
# Actions Module
######################################################################

import jinja2
import syslog
import time


def failed(redata, jdata, rdb, r_server):
    ''' This method will be called when a monitor has failed '''
    run = True
    # Check for Trigger
    if redata['trigger'] > jdata['failcount']:
        run = False

    # Check for lastrun
    checktime = time.time() - float(redata['lastrun'])
    if checktime < redata['frequency'] or checktime < 900:
        run = False

    if run:
        result = emailNotify(redata, jdata, "failed.msg")
        if result:
            line = "enotify: Sent %s email notification for monitor %s" % (
                jdata['check']['status'], jdata['cid'])
            syslog.syslog(syslog.LOG_INFO, line)
            return True
        else:
            line = "enotify: Failed to send %s email notification for monitor %s" % (jdata['check']['status'], jdata['cid'])
            syslog.syslog(syslog.LOG_ERR, line)
            return False
    else:
        line = "enotify: Skipping %s email notification for monitor %s" % (
            jdata['check']['status'], jdata['cid'])
        syslog.syslog(syslog.LOG_ERR, line)
        return None


def healthy(redata, jdata, rdb, r_server):
    ''' This method will be called when a monitor has passed '''
    run = True
    if "healthy" in jdata['check']['prev_status']:
        run = False

    if "send_healthy" in redata['data']:
        if redata['data']['send_healthy'] == "False":
            run = False

    if run:
        result = emailNotify(redata, jdata, "healthy.msg")
        if result:
            line = "enotify: Sent %s email notification for monitor %s" % (
                jdata['check']['status'], jdata['cid'])
            syslog.syslog(syslog.LOG_INFO, line)
            return True
        else:
            line = "enotify: Failed to send %s email notification for monitor %s" % (jdata['check']['status'], jdata['cid'])
            syslog.syslog(syslog.LOG_ERR, line)
            return False
    else:
        line = "enotify: Skipping %s email notification for monitor %s" % (
            jdata['check']['status'], jdata['cid'])
        syslog.syslog(syslog.LOG_INFO, line)
        return None


def emailNotify(redata, jdata, tfile):
    '''
    This method will be called to notify a user via email of status changes
    '''
    import yaml
    import requests
    import json
    # TODO: I hate reading the config file in should look at reaction failed/healthy
    # definitions to find a better way of doing this
    configfile = "config/config.yml"
    cfh = open(configfile, "r")
    config = yaml.safe_load(cfh)
    cfh.close()

    data = {}
    templateLoader = jinja2.FileSystemLoader(
        searchpath="/data/crbridge/templates/")
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template(tfile)

    data['name'] = jdata['name']
    msg = template.render(data)

    mandrill_data = {
        "key": config['mandrill_api_key'],
        "message": {
            "text": msg,
            "from_email": "noreply@runbook.io",
            "from_name" : "Runbook Notifications",
            "subject" : "Monitor Alerts",
            "to" : [
                { "email": redata['data']['email'] }
            ]
        },
        "async" : True
    }

    payload = json.dumps(mandrill_data)
    url = config['mandrill_api_url'] + "/messages/send.json"
    try:
        result = requests.post(url=url, data=payload, timeout=1.0, verify=True)
    except:
        return False
    if result.status_code >= 200 and result.status_code <= 299:
      return True
    else:
      line = "enotify: Got status code %d from mandrill for monitor %s" % (
            result.status_code, jdata['cid'])
      return False
