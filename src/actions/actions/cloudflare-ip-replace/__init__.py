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
import requests
import json
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
        edit(redata, jdata, r_server, failback=False, logger)
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
        if "failback" in redata['data']:
            if redata['data']['failback'] == "automatic":
                edit(redata, jdata, r_server, failback=True, logger)
        else:
            # Do nothing to prevent unplanned failback
            line = "cloudflare-ip-replace: Monitor is true, nothing to do"
            logger.info(line)
        return True
    else:
        return None


# Locals
def edit(redata, jdata, r_server, failback=False, logger):
    ''' Edit DNS Records '''
    usrdata = {'z': redata['data']['domain'],
               'tkn': redata['data']['apikey'],
               'email': redata['data']['email']}
    key = 'cf-replace:' + jdata['cid'] + ':' + redata['id']
    runcount = 0
    if failback is True:
        records = r_server.smembers(key + ":deleted")
        for rec in records:
            rstring = r_server.get(key + ":" + rec)
            if rstring is not None:
                data = json.loads(rstring)
                data['id'] = rec
                result = editRecord(data)
                if result:
                    dkey = key + ":" + rec
                    r_server.delete(dkey)
                    skey = key + ":deleted"
                    r_server.srem(skey, rec)
                    line = "cloudflare-ip-replace: Record %s changed to IP %s" % (
                        data['id'], data['content'])
                    logger.debug(line)
                else:
                    line = "cloudflare-ip-replace: False to change record %s" % data['id']
                    logger.debug(line)
            else:
                skey = key + ":deleted"
                r_server.srem(skey, rec)
                line = "cloudflare-ip-replace: False to change record %s - Not found in Redis, removed from record list" % rec
                logger.debug(line)
            runcount = runcount + 1
    else:
        falsedata, failcount = checkZone(redata['data']['ip'], usrdata)
        line = "cloudflare-ip-replace: Found %d false records" % failcount
        logger.debug(line)
        for rec in falsedata.keys():
            data = usrdata
            for item in falsedata[rec].keys():
                data[item] = falsedata[rec][item]
            rstring = json.dumps(data)
            data['content'] = redata['data']['replaceip']
            data['id'] = rec
            result = editRecord(data)
            if result:
                if redata['data']['failback'] == "automatic":
                    r_server.set(key + ":" + rec, rstring)
                    r_server.sadd(key + ":deleted", rec)
                line = "cloudflare-ip-replace: Record %s changed to IP %s" % (
                    data['id'], data['content'])
                logger.debug(line)
            else:
                line = "cloudflare-ip-replace: False to edit record %s" % data[
                    'id']
                logger.debug(line)
            runcount = runcount + 1
    line = "cloudflare-ip-replace: Actioned %d records" % runcount
    logger.debug(line)
    return True


def callAPI(reqdata):
    ''' Call the CloudFlare API '''
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    try:
        req = requests.post(
            url="https://www.cloudflare.com/api_json.html",
            data=reqdata, headers=headers)
    except:
        response = {'result': 'false'}
        return response

    if req.status_code == 200:
        response = json.loads(req.text)
        return response
    else:
        response = {'result': 'false'}
        return response


def checkZone(ip, usrdata):
    ''' Check the zone for the IP specified '''
    false = {}
    usrdata['a'] = 'rec_load_all'
    response = callAPI(usrdata)
    runcount = 0
    if response['result'] == "success":
        for record in response['response']['recs']['objs']:
            if record['content'] == ip:
                runcount = runcount + 1
                false[record['rec_id']] = {'type': record["type"],
                                            'name': record["name"],
                                            'content': record["content"],
                                            'service_mode': record["service_mode"],
                                            'ttl': record["ttl"],
                                            'prio': record["prio"]}
    return false, runcount


def editRecord(data):
    ''' Edit the DNS Record '''
    data['a'] = 'rec_edit'
    response = callAPI(data)
    if response['result'] == "success":
        return True
    else:
        return False
