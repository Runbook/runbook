#!/usr/bin/python
######################################################################
# Cloud Routes Bridge
# -------------------------------------------------------------------
# Actions Module
######################################################################

import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
import time
import syslog


def false(redata, jdata, rdb, r_server):
    ''' This method will be called when a monitor has false '''
    if redata['reaction_return'] is True:
        chlastrun(redata['id'], rdb, r_server)
        return True
    else:
        return None


def true(redata, jdata, rdb, r_server):
    ''' This method will be called when a monitor has passed '''
    if redata['reaction_return'] is True:
        chlastrun(redata['id'], rdb, r_server)
        return True
    else:
        return None


def chlastrun(rid, rdb, r_server):
    ''' This method will be called to change a users status in the db '''
    lastrun = time.time()
    success = False
    cacheonly = False

    # First set rethinkdb
    try:
        results = r.table('reactions').get(
            rid).update({'lastrun': lastrun}).run(rdb)
        if results['replaced'] == 1:
            line = "update-lastrun: RethinkDB lastrun for %s is now set to: %r" % (rid, lastrun)
            syslog.syslog(syslog.LOG_INFO, line)
            success = True
        else:
            success = False
            cacheonly = True
    except (RqlRuntimeError, RqlDriverError) as e:
        line = "update-lastrun: Rethinkdb is inaccessible cannot change lastrun for %s" % rid
        syslog.syslog(syslog.LOG_INFO, line)
        line = "update-lastrun: Rethinkdb Error: %s" % e.message
        syslog.syslog(syslog.LOG_INFO, line)
        success = False
        cacheonly = True

    # Then set redis cache
    try:
        r_server.hset("reaction:" + rid, 'lastrun', lastrun)
        line = "update-lastrun: Redis lastrun for %s is now set to: %r" % (
            rid, lastrun)
        syslog.syslog(syslog.LOG_INFO, line)
        success = True
    except:
        line = "update-lastrun: Redis is inaccessible cannot change lastrun for %s" % rid
        syslog.syslog(syslog.LOG_INFO, line)
        success = False

    return success
