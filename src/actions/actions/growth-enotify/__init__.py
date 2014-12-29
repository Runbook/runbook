#!/usr/bin/python
######################################################################
# Cloud Routes Bridge
# -------------------------------------------------------------------
# Actions Module
######################################################################

import smtplib
import jinja2
import time


def action(**kwargs):
    ''' This method is called to action a reaction '''
    # This method can be used for legacy reactions that have
    # a different function based on true/false
    logger = kwargs['logger']
    if "false" in kwargs['jdata']['check']['status']:
        return false(kwargs['redata'], kwargs['jdata'],
            kwargs['rdb'], kwargs['r_server'], logger)
    if "true" in kwargs['jdata']['check']['status']:
        return true(kwargs['redata'], kwargs['jdata'],
            kwargs['rdb'], kwargs['r_server'], logger)


def false(redata, jdata, rdb, r_server, logger):
    ''' This method will be called when a monitor has false '''
    run = True
    # Check for Trigger
    if redata['trigger'] > jdata['failcount']:
        run = False

    # Check for lastrun
    checktime = time.time() - float(redata['lastrun'])
    if checktime < redata['frequency'] or checktime < 900:
        run = False

    if run:
        result = emailNotify(redata, jdata, "growth-false.msg", logger)
        if result:
            line = "growth-enotify: Sent %s email notification for monitor %s" % (
                jdata['check']['status'], jdata['cid'])
            logger.info(line)
            return True
        else:
            line = "growth-enotify: False to send %s email notification for monitor %s" % (jdata['check']['status'], jdata['cid'])
            logger.error(line)
            return False
    else:
        line = "growth-enotify: Skipping %s email notification for monitor %s" % (
            jdata['check']['status'], jdata['cid'])
        logger.error(line)
        return None


def true(redata, jdata, rdb, r_server, logger):
    ''' This method will be called when a monitor has passed '''
    run = True
    if "true" in jdata['check']['prev_status']:
        run = False

    if "send_true" in redata['data']:
        if redata['data']['send_true'] == "False":
            run = False

    if run:
        result = emailNotify(redata, jdata, "growth-true.msg", logger)
        if result:
            line = "growth-enotify: Sent %s email notification for monitor %s" % (
                jdata['check']['status'], jdata['cid'])
            logger.info(line)
            return True
        else:
            line = "growth-enotify: False to send %s email notification for monitor %s" % (jdata['check']['status'], jdata['cid'])
            logger.error(line)
            return False
    else:
        line = "growth-enotify: Skipping %s email notification for monitor %s" % (
            jdata['check']['status'], jdata['cid'])
        logger.error(line)
        return None

def emailNotify(redata, jdata, tfile, logger):
    '''
    This method will be called to notify a user via email of status changes
    '''
    import yaml
    import requests
    import json
    # TODO: I hate reading the config file in should look at reaction false/true
    # definitions to find a better way of doing this
    configfile = "config/config.yml"
    cfh = open(configfile, "r")
    config = yaml.safe_load(cfh)
    cfh.close()

    data = {}
    templateLoader = jinja2.FileSystemLoader(
        searchpath="./templates/")
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template(tfile)

    data['name'] = jdata['name']
    msg = template.render(data)

    mandrill_data = {
        "key": config['mandrill_api_key'],
        "message": {
            "text": msg,
            "from_email": "noreply@runbook.io",
            "from_name": "Runbook Notifications",
            "subject": "Heads up! %s is down" % jdata['name'],
            "to": [
                {"email": redata['data']['email']}
            ]
        },
        "async": True
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
        logger.warning(line)
        return False
