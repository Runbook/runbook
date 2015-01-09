#!/usr/bin/python
######################################################################
# Cloud Routes Bridge
# -------------------------------------------------------------------
# Actions Module
######################################################################

import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
import time
import json

def action(**kwargs):
    ''' This method is called to action a reaction '''
    redata = kwargs['redata']
    jdata = kwargs['jdata']
    rdb = kwargs['rdb']
    r_server = kwargs['r_server']
    logger = kwargs['logger']
    return logit(jdata, rdb, r_server, logger)

def logit(jdata, rdb, r_server, logger):
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
        line = "logit-monitor: RethinkDB is inaccessible cannot log %s, sending to redis" % jdata['cid']
        logger.info(line)
        line = "logit-monitor: RethinkDB Error: %s" % e.message
        logger.info(line)
        try:
            # Then set redis cache
            ldata = json.dumps(transaction)
            r_server.sadd("history", ldata)
            success = True
        except:
            line = "logit-monitor: Redis is inaccessible cannot log %s, via redis" % jdata['cid']
            logger.info(line)
            success = False
    return success
