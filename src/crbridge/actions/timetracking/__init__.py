#!/usr/bin/python
######################################################################
# Cloud Routes Bridge
# -------------------------------------------------------------------
# Actions Module
######################################################################

import stathat
import time
import syslog


def failed(redata, jdata, rdb, r_server):
    ''' This method will be called when a monitor has failed '''
    updateStathat(jdata)
    return True


def healthy(redata, jdata, rdb, r_server):
    ''' This method will be called when a monitor has passed '''
    updateStathat(jdata)
    return True


def updateStathat(jdata):
    ''' This method will be called to update a stathat Statistic '''
    ez_key = jdata['time_tracking']['ez_key']
    stat_name = "[%s] End to End Monitor transaction time" % jdata[
        'time_tracking']['env']
    value = time.time() - jdata['time_tracking']['control']
    stathat.ez_value(ez_key, stat_name, value)
    line = "timetracker: Sent stat to StatHat for %s" % jdata['cid']
    syslog.syslog(syslog.LOG_INFO, line)
