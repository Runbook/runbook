#!/usr/bin/python
#####################################################################
# Cloud Routes: CloudFlail Actions Module
# ------------------------------------------------------------------
# Description:
# ------------------------------------------------------------------
# This module is used to failover and failback domains after
# untrue and true checks.
# ------------------------------------------------------------------
# Version: Alpha.20140424
# Original Author: Benjamin J. Cane - madflojo@cloudrout.es
# Contributors:
# - your name here
#####################################################################

# Data sources

# Action Helpers
import cloudflail

import time

def action(**kwargs):
    ''' This method is called to action a reaction '''
    # This method can be used for legacy reactions that have
    # a different function based on true/false
    logger = kwargs['logger']
    if "false" in kwargs['jdata']['check']['status']:
        return false(kwargs['redata'], kwargs['jdata'],
            kwargs['rdb'], kwargs['r_server'], logger)
    if "true" in kwargs['jdata']['check']['status']:
        return true(kwargs['redata'], kwargs['jdata'],
            kwargs['rdb'], kwargs['r_server'], logger)


def false(redata, jdata, rdb, r_server, logger):
    ''' This method will be called when a monitor has false '''
    run = True
    # Check for Trigger
    if redata['trigger'] > jdata['failcount']:
        run = False

    # Check for lastrun
    checktime = time.time() - float(redata['lastrun'])
    if checktime < redata['frequency']:
        run = False

    if run:
        remove(redata, jdata, r_server, logger)
        return True
    else:
        return None


def true(redata, jdata, rdb, r_server, logger):
    ''' This method will be called when a monitor has passed '''
    run = True
    # Check for Trigger
    if redata['trigger'] > jdata['failcount']:
        run = False

    # Check for lastrun
    checktime = time.time() - float(redata['lastrun'])
    if checktime < redata['frequency']:
        run = False

    if run:
        readd(redata, jdata, r_server, logger)
        return True
    else:
        return None


# Locals

def remove(redata, jdata, r_server, logger):
    ''' Perform the ip removal '''
    usrdata = [
        ('z', redata['data']['domain']),
        ('tkn', redata['data']['apikey']),
        ('email', redata['data']['email'])]
    zone = redata['data']['domain']

    # Check the CloudFlare Zone
    falserecs, falsedata = cloudflail.checkZone(
        redata['data']['ip'], usrdata)
    numrecs = len(falserecs)
    if numrecs > 0:
        line = "cloudflare-ip-remove: %d records found to remove" % numrecs
        logger.debug(line)
        for rec in falserecs:
            result = cloudflail.delRecord(rec, usrdata)
            if result:
                # Log Removal to Redis for later checks
                key = 'domains:' + jdata['cid'] + ':' + zone + ':' + rec
                rdata = falsedata[rec]
                for item in rdata.keys():
                    r_server.set(key + ":" + item, rdata[item])
                r_server.sadd(
                    'domains:' + jdata['cid'] + ':' + zone + ':' + rdata["content"] + ':deleted', rec)
                # Log in jdata success
                line = "cloudflare-ip-remove: Removal of record %s successful" % rec
                logger.info(line)
            else:
                line = "cloudflare-ip-remove: Removal of record %s false" % rec
                logger.info(line)
    else:
        line = "cloudflare-ip-remove: IP %s not found in zone" % redata[
            'data']['ip']
        logger.debug(line)
    return True


def readd(redata, jdata, r_server, replaceip=Non, logger):
    ''' Perform the ip readd '''

    usrdata = [
        ('z', redata['data']['domain']),
        ('tkn', redata['data']['apikey']),
        ('email', redata['data']['email'])]
    zone = redata['data']['domain']
    ip = redata['data']['ip']

    # Try and readd all removed zones
    readds = len(r_server.smembers(
        "domains:" + jdata['cid'] + ':' + zone + ":" + ip + ":deleted"))
    try:
        for item in range(0, readds + 1):
            deleted = r_server.spop(
                "domains:" + jdata['cid'] + ':' + zone + ":" + ip + ":deleted")
            add_data = []
            key = "domains:" + jdata['cid'] + ':' + zone + ":" + deleted + ":"
            ztype = r_server.get(key + "type")
            r_server.delete(key + "type")
            add_data.append(('type', ztype))

            ttl = r_server.get(key + "ttl")
            r_server.delete(key + "ttl")
            add_data.append(('ttl', ttl))

            name = r_server.get(key + "name")
            r_server.delete(key + "name")
            add_data.append(('name', name))

            if replaceip is None:
                content = r_server.get(key + "content")
                r_server.delete(key + "content")
            else:
                content = replaceip
                r_server.delete(key + "content")
            add_data.append(('content', content))

            service_mode = r_server.get(key + "service_mode")
            r_server.delete(key + "service_mode")
            add_data.append(('service_mode', service_mode))

            if ztype == "MX":
                prio = r_server.get(key + "prio")
                add_data.append(('prio', prio))
            r_server.delete(key + "prio")

            if service_mode == "1":
                result = cloudflail.addRecord(
                    add_data, usrdata, service_mode=True)
            else:
                result = cloudflail.addRecord(add_data, usrdata)
            if result:
                line = "cloudflare-ip-remove: Readding record %s to zone %s successful" % (name, zone)
                logger.info(line)
            else:
                line = "cloudflare-ip-remove: Readding record %s to zone %s false" % (name, zone)
                logger.info(line)
    except TypeError:
        line = "cloudflare-ip-remove: No records for ip %s in deleted queue for zone %s" % (ip, zone)
        logger.info(line)
    return True
