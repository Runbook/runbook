#!/usr/bin/python
######################################################################
# Cloud Routes Bridge
# -------------------------------------------------------------------
# Actions Module
######################################################################

import smtplib
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
    data = {}
    templateLoader = jinja2.FileSystemLoader(
        searchpath="/data/crbridge/templates/")
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template(tfile)

    data['email'] = redata['data']['email']
    data['name'] = jdata['name']
    msg = template.render(data)

    sender = 'noreply@runbook.io'
    receivers = [data['email']]

    try:
        smtp = smtplib.SMTP(host='post01.snxdesigns.com', port=587)
        smtp.sendmail(sender, receivers, msg)
        return True
    except:
        return False
