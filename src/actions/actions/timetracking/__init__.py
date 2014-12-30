#!/usr/bin/python
######################################################################
# Cloud Routes Bridge
# -------------------------------------------------------------------
# Actions Module
######################################################################

import stathat
import time

def action(**kwargs):
    ''' This method is called to action a reaction '''
    logger = kwargs['logger']
    updateStathat(kwargs['jdata'], logger)
    return True


def updateStathat(jdata, logger):
    ''' This method will be called to update a stathat Statistic '''
    ez_key = jdata['time_tracking']['ez_key']
    stat_name = "[%s] End to End Monitor transaction time" % jdata[
        'time_tracking']['env']
    value = time.time() - jdata['time_tracking']['control']
    stathat.ez_value(ez_key, stat_name, value)
    line = "timetracker: Sent stat to StatHat for %s" % jdata['cid']
    logger.info(line)
