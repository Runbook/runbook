#!/usr/bin/python
######################################################################
# Cloud Routes Bridge
# -------------------------------------------------------------------
# Actions Module
######################################################################

import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
import syslog
import redis
import time
import json


def failed(redata, jdata, rdb, r_server):
    ''' This method will be called when a monitor has failed '''
    result = logit(jdata, rdb, r_server)
    return result


def healthy(redata, jdata, rdb, r_server):
    ''' This method will be called when a monitor has passed '''
    result = logit(jdata, rdb, r_server)
    return result


def logit(jdata, rdb, r_server):
    ''' This method will be called to log monitor transaction history '''
    transaction = {
        'cid': jdata['cid'],
        'type': "monitor",
        'starttime': jdata['time_tracking']['control'],
        'zone': jdata['zone'],
        'uid': jdata['uid'],
        'url': jdata['url'],
        'failcount': jdata['failcount'],
        'status': jdata['check']['status'],
        'method': jdata['check']['method'],
        'time': time.time(),
        'cacheonly': jdata['cacheonly'],
        'name': jdata['name']
    }
    success = False
    cacheonly = False

    # Try to set rethinkdb first
    try:
        results = r.table('history').insert(transaction).run(rdb)
        if results['inserted'] == 1:
            success = True
            cacheonly = False
        else:
            success = False
    except (RqlDriverError, RqlRuntimeError) as e:
        success = False
        cacheonly = True
        line = "logit-monitor: RethinkDB is inaccessible cannot log %s, sending to redis" % jdata[
            'cid']
        syslog.syslog(syslog.LOG_INFO, line)
        line = "logit-monitor: RethinkDB Error: %s" % e.message
        syslog.syslog(syslog.LOG_INFO, line)
        try:
            # Then set redis cache
            ldata = json.dumps(transaction)
            r_server.sadd("history", ldata)
            success = True
        except:
            line = "logit-monitor: Redis is inaccessible cannot log %s, via redis" % jdata[
                'cid']
            syslog.syslog(syslog.LOG_INFO, line)
            success = False
    return success
