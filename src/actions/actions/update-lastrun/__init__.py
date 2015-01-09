#!/usr/bin/python
######################################################################
# Cloud Routes Bridge
# -------------------------------------------------------------------
# Actions Module
######################################################################

import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
import time

def action(**kwargs):
    ''' This method is called to action a reaction '''
    redata = kwargs['redata']
    rdb = kwargs['rdb']
    r_server = kwargs['r_server']
    logger = kwargs['logger']
    if redata['reaction_return'] is True:
        chlastrun(redata['id'], rdb, r_server, logger)
        return True
    else:
        return None


def chlastrun(rid, rdb, r_server, logger):
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
            logger.info(line)
            success = True
        else:
            success = False
            cacheonly = True
    except (RqlRuntimeError, RqlDriverError) as e:
        line = "update-lastrun: Rethinkdb is inaccessible cannot change lastrun for %s" % rid
        logger.info(line)
        line = "update-lastrun: Rethinkdb Error: %s" % e.message
        logger.info(line)
        success = False
        cacheonly = True

    # Then set redis cache
    try:
        r_server.hset("reaction:" + rid, 'lastrun', lastrun)
        line = "update-lastrun: Redis lastrun for %s is now set to: %r" % (
            rid, lastrun)
        logger.info(line)
        success = True
    except:
        line = "update-lastrun: Redis is inaccessible cannot change lastrun for %s" % rid
        logger.info(line)
        success = False

    return success
