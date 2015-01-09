#!/usr/bin/python
######################################################################
# Cloud Routes Bridge
# -------------------------------------------------------------------
# Actions Module
######################################################################

import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError, RqlDriverError

def action(**kwargs):
    ''' This method is called to action a reaction '''
    jdata = kwargs['jdata']
    rdb = kwargs['rdb']
    logger = kwargs['logger']
    r_server = kwargs['r_server']
    if jdata['check']['prev_status'] != jdata['check']['status']:
        chStatus(jdata['cid'], jdata['check']['status'], rdb, r_server, logger)
        if "web" in jdata['check']['status']:
            # Web Checks always get an increased failcount
            incFailcount(jdata['cid'],
                jdata['prev_failcount'], rdb, r_server, logger)
        else:
            # Reset failcount as status is different
            resetFailcount(jdata['cid'], rdb, r_server, logger)
    else:
        # Increase failcount for each returned status
        incFailcount(jdata['cid'],
            jdata['prev_failcount'], rdb, r_server, logger)
    return True


def chStatus(cid, status, rdb, r_server, logger):
    ''' This method will be called to change a users status in the db '''
    success = False
    cacheonly = False

    # Try to set rethinkdb first
    try:
        results = r.table('monitors').get(
            cid).update({'status': status}).run(rdb)
        if results['replaced'] == 1:
            success = True
            cacheonly = False
        else:
            success = False
    except (RqlDriverError, RqlRuntimeError) as e:
        success = False
        cacheonly = True
        line = "chstatus: RethinkDB is inaccessible cannot change status for %s" % cid
        logger.info(line)
        line = "chstatus: RethinkDB Error: %s" % e.message
        logger.info(line)

    # Then set redis cache
    try:
        r_server.hset("monitor:" + cid, 'status', status)
        success = True
    except:
        line = "chstatus: Redis is inaccessible cannot change status for %s" % cid
        logger.info(line)
        success = False

    return success


def resetFailcount(cid, rdb, r_server, logger):
    ''' This method will reset a users failcount '''
    failcount = 0
    success = False
    cacheonly = False

    # Try to set rethinkdb first
    try:
        results = r.table('monitors').get(cid).update(
            {'failcount': failcount}).run(rdb)
        if results['replaced'] == 1:
            success = True
            cacheonly = False
        else:
            success = False
    except (RqlDriverError, RqlRuntimeError) as e:
        success = False
        cacheonly = True
        line = "chstatus: RethinkDB is inaccessible cannot change failcount for %s" % cid
        logger.info(line)
        line = "chstatus: RethinkDB Error: %s" % e.message
        logger.info(line)

    # Then set redis cache
    try:
        r_server.hset("monitor:" + cid, 'failcount', failcount)
        success = True
    except:
        line = "chstatus: Redis is inaccessible cannot change failcount for %s" % cid
        logger.info(line)
        success = False

    return success


def incFailcount(cid, failcount, rdb, r_server, logger):
    ''' This method will increase a users failcount '''
    failcount = int(failcount) + 1
    success = False
    cacheonly = False

    # Try to set rethinkdb first
    try:
        results = r.table('monitors').get(cid).update(
            {'failcount': failcount}).run(rdb)
        if results['replaced'] == 1:
            success = True
            cacheonly = False
        else:
            success = False
    except (RqlDriverError, RqlRuntimeError) as e:
        success = False
        cacheonly = True
        line = "chstatus: RethinkDB is inaccessible cannot change failcount for %s" % cid
        logger.info(line)
        line = "chstatus: RethinkDB Error: %s" % e.message
        logger.info(line)

    # Then set redis cache
    try:
        r_server.hset("monitor:" + cid, 'failcount', failcount)
        success = True
    except:
        line = "chstatus: Redis is inaccessible cannot change failcount for %s" % cid
        logger.info(line)
        success = False

    return success
