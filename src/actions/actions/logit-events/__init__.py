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

def action(**kwargs):
    ''' This method is called to action a reaction '''
    redata = kwargs['redata']
    jdata = kwargs['jdata']
    rdb = kwargs['rdb']
    r_server = kwargs['r_server']

    run = True
    if jdata['check']['prev_status'] == jdata['check']['status']:
         run = False 

    if run:
        return logit(jdata, rdb, r_server)
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
