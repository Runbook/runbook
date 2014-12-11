#!/usr/bin/python
######################################################################
# Cloud Routes Bridge
# -------------------------------------------------------------------
# Actions Module
######################################################################

import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
import syslog


def false(redata, jdata, rdb, r_server):
    ''' This method will be called when a monitor has false '''
    if jdata['check']['prev_status'] != "false":
        if jdata['check']['status'] == "web-false":
            result = chStatus(jdata['cid'], "web-false", rdb, r_server)
            # Manuals are always increased
            incFailcount(jdata['cid'], jdata['failcount'], rdb, r_server)
        else:
            result = chStatus(jdata['cid'], "false", rdb, r_server)
            # Reset failcounter
            resetFailcount(jdata['cid'], rdb, r_server)
        if result:
            line = "chstatus: Setting monitor %s status to false" % jdata['cid']
            syslog.syslog(syslog.LOG_INFO, line)
            return True
        else:
            line = "chstatus: Error setting monitor %s status to false" % jdata['cid']
            syslog.syslog(syslog.LOG_ERR, line)
            return False
    else:
        line = "chstatus: skipping status change as monitor %s status is already false" % jdata['cid']
        syslog.syslog(syslog.LOG_INFO, line)
        # Auto increase failcount which isn't just for fails
        incFailcount(jdata['cid'], jdata['failcount'], rdb, r_server)

    return True


def true(redata, jdata, rdb, r_server):
    ''' This method will be called when a monitor has passed '''
    if jdata['check']['prev_status'] != "true":
        result = chStatus(jdata['cid'], "true", rdb, r_server)
        # Reset failcounter
        resetFailcount(jdata['cid'], rdb, r_server)
        if result:
            line = "chstatus: Setting monitor %s status to true" % jdata[
                'cid']
            syslog.syslog(syslog.LOG_INFO, line)
            return True
        else:
            line = "chstatus: Error setting monitor %s status to true" % jdata['cid']
            syslog.syslog(syslog.LOG_ERR, line)
            return False
    else:
        # Auto increase failcount which isn't just for fails
        incFailcount(jdata['cid'], jdata['failcount'], rdb, r_server)
        line = "chstatus: skipping status change as monitor %s status is already true" % jdata['cid']
        syslog.syslog(syslog.LOG_INFO, line)

    return True


def chStatus(cid, status, rdb, r_server):
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
        syslog.syslog(syslog.LOG_INFO, line)
        line = "chstatus: RethinkDB Error: %s" % e.message
        syslog.syslog(syslog.LOG_INFO, line)

    # Then set redis cache
    try:
        r_server.hset("monitor:" + cid, 'status', status)
        success = True
    except:
        line = "chstatus: Redis is inaccessible cannot change status for %s" % cid
        syslog.syslog(syslog.LOG_INFO, line)
        success = False

    return success


def resetFailcount(cid, rdb, r_server):
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
        syslog.syslog(syslog.LOG_INFO, line)
        line = "chstatus: RethinkDB Error: %s" % e.message
        syslog.syslog(syslog.LOG_INFO, line)

    # Then set redis cache
    try:
        r_server.hset("monitor:" + cid, 'failcount', failcount)
        success = True
    except:
        line = "chstatus: Redis is inaccessible cannot change failcount for %s" % cid
        syslog.syslog(syslog.LOG_INFO, line)
        success = False

    return success


def incFailcount(cid, failcount, rdb, r_server):
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
        syslog.syslog(syslog.LOG_INFO, line)
        line = "chstatus: RethinkDB Error: %s" % e.message
        syslog.syslog(syslog.LOG_INFO, line)

    # Then set redis cache
    try:
        r_server.hset("monitor:" + cid, 'failcount', failcount)
        success = True
    except:
        line = "chstatus: Redis is inaccessible cannot change failcount for %s" % cid
        syslog.syslog(syslog.LOG_INFO, line)
        success = False

    return success
