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
import json


def false(redata, jdata, rdb, r_server):
    ''' This method will be called when a monitor has false '''
    result = logit(redata, jdata, rdb, r_server)
    return result


def true(redata, jdata, rdb, r_server):
    ''' This method will be called when a monitor has passed '''
    result = logit(redata, jdata, rdb, r_server)
    return result


def logit(redata, jdata, rdb, r_server):
    ''' This method will be called to log monitor transaction history '''
    transaction = {
        'cid': jdata['cid'],
        'type': "reaction",
        'rid': redata['id'],
        'starttime': jdata['time_tracking']['control'],
        'zone': jdata['zone'],
        'uid': jdata['uid'],
        'url': jdata['url'],
        'trigger': redata['trigger'],
        'lastrun': redata['lastrun'],
        'rstatus': "executed",
        'status': jdata['check']['status'],
        'method': jdata['check']['method'],
        'time': time.time(),
        'cacheonly': redata['cacheonly'],
        'name': redata['name']
    }
    success = False
    cacheonly = False
    if redata['reaction_return'] is True:
        transaction['rstatus'] = 'Executed'
    elif redata['reaction_return'] is None:
        transaction['rstatus'] = 'Skipped'
    elif redata['reaction_return'] is False:
        transaction['rstatus'] = 'False'
    else:
        transaction['rstatus'] = 'Unknown'

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
        line = "logit-reaction: RethinkDB is inaccessible cannot log %s, sending to redis" % jdata['cid']
        syslog.syslog(syslog.LOG_INFO, line)
        line = "logit-reaction: RethinkDB Error: %s" % e.message
        syslog.syslog(syslog.LOG_INFO, line)
        try:
            # Then set redis cache
            ldata = json.dumps(transaction)
            r_server.sadd("history", ldata)
            success = True
        except:
            line = "logit-reaction: Redis is inaccessible cannot log %s, via redis" % jdata['cid']
            syslog.syslog(syslog.LOG_INFO, line)
            success = False
    return success
