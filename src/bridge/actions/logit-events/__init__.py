#!/usr/bin/python
######################################################################
# Cloud Routes Bridge
# -------------------------------------------------------------------
# Actions Module
######################################################################

import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
import syslog
import time
import datetime
import json


def false(redata, jdata, rdb, r_server):
    ''' This method will be called when a monitor has false '''
    run = True
    if "false" in jdata['check']['prev_status']:
        run = False

    if run:
        result = logit(jdata, rdb, r_server)
        return result
    else:
        return None


def true(redata, jdata, rdb, r_server):
    ''' This method will be called when a monitor has passed '''
    run = True
    if "true" in jdata['check']['prev_status']:
        run = False

    if run:
        result = logit(jdata, rdb, r_server)
        return result
    else:
        return None


def logit(jdata, rdb, r_server):
    ''' This method will be called to log monitor transaction history '''
    etime = time.time()
    transaction = {
        'cid': jdata['cid'],
        'type': "monitor",
        'zone': jdata['zone'],
        'uid': jdata['uid'],
        'failcount': jdata['failcount'],
        'prev_failcount': jdata['prev_failcount'],
        'status': jdata['check']['status'],
        'prev_status': jdata['check']['prev_status'],
        'method': jdata['check']['method'],
        'time': etime,
        'time_friendly': datetime.datetime.fromtimestamp(etime).strftime('%Y-%m-%d %H:%M:%S'),
        'cacheonly': jdata['cacheonly'],
        'name': jdata['name']
    }
    success = False
    cacheonly = False

    # Try to set rethinkdb first
    try:
        results = r.table('events').insert(transaction).run(rdb)
        if results['inserted'] == 1:
            success = True
            cacheonly = False
        else:
            success = False
    except (RqlDriverError, RqlRuntimeError) as e:
        success = False
        cacheonly = True
        line = "logit-events: RethinkDB is inaccessible cannot log %s, sending to redis" % jdata[
            'cid']
        syslog.syslog(syslog.LOG_INFO, line)
        line = "logit-events: RethinkDB Error: %s" % e.message
        syslog.syslog(syslog.LOG_INFO, line)
        try:
            # Then set redis cache
            ldata = json.dumps(transaction)
            r_server.sadd("events", ldata)
            success = True
        except:
            line = "logit-events: Redis is inaccessible cannot log %s, via redis" % jdata[
                'cid']
            syslog.syslog(syslog.LOG_INFO, line)
            success = False
    return success
