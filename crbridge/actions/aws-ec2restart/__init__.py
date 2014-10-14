#!/usr/bin/python
######################################################################
# Cloud Routes Bridge
# -------------------------------------------------------------------
# Actions Module
######################################################################

import syslog
import boto.ec2
import time


def failed(redata, jdata, rdb, r_server):
    ''' This method will be called when a monitor has failed '''
    run = True
    # Check for Trigger
    if redata['trigger'] > jdata['failcount']:
        run = False

    # Check for lastrun
    checktime = time.time() - float(redata['lastrun'])
    if checktime < redata['frequency']:
        run = False

    if redata['data']['call_on'] == 'healthy':
        run = False

    if run:
        return actionEC2(redata, jdata)
    else:
        return None


def healthy(redata, jdata, rdb, r_server):
    ''' This method will be called when a monitor has passed '''
    run = True
    # Check for Trigger
    if redata['trigger'] > jdata['failcount']:
        run = False

    # Check for lastrun
    checktime = time.time() - float(redata['lastrun'])
    if checktime < redata['frequency']:
        run = False

    if redata['data']['call_on'] == 'failed':
        run = False

    if run:
        return actionEC2(redata, jdata)
    else:
        return None


def actionEC2(redata, jdata):
    ''' Perform EC2 Actions '''
    try:
        conn = boto.ec2.connect_to_region(
            redata['data']['region'],
            aws_access_key_id=redata['data']['aws_access_key'],
            aws_secret_access_key=redata['data']['aws_secret_key'])
        try:
            instances = conn.get_only_instances(
                instance_ids=[redata['data']['instance_id']])
            instances[0].reboot()
            return True
        except:
            return False
    except:
        line = "aws-ec2restart: Could not connect to AWR for monitor %s" % jdata['cid']
        syslog.syslog(syslog.LOG_INFO, line)
        return False
