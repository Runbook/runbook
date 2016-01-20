# Update CloudFlare DNS record

# Action Helpers
import cloudflare
import json
import time


def action(**kwargs):
    ''' This method is called to action a reaction '''
    redata = kwargs['redata']
    jdata = kwargs['jdata']
    logger = kwargs['logger']
    r_server = kwargs['r_server']
    run = True
    revert = True
    # Check for Trigger
    if redata['trigger'] > jdata['failcount']:
        run = False
        revert = False

    # Check for lastrun
    checktime = time.time() - float(redata['lastrun'])
    if checktime < redata['frequency']:
        run = False
        revert = False

    if redata['data']['call_on'] not in jdata['check']['status']:
        run = False

    if run:
        return run_reaction(redata, jdata, logger, r_server)
    else:
        if revert:
            return revert_reaction(redata, jdata, logger, r_server)
        else:
            return None

def revert_reaction(redata, jdata, logger, r_server):
    ''' This method reverts the heavy lifting '''
    readded = 0
    result = r_server.smembers("cloudflare-dns-failover:%s:%s" %
                               (jdata['cid'], redata['id']))
    if len(result) < 1:
        logger.debug("cloudflare-dns-failover: no removed records found")
        return None
    zoneid = cloudflare.get_zoneid(redata['data']['email'],
                                   redata['data']['apikey'],
                                   redata['data']['domain'],
                                   logger)
    if zoneid is None:
        logger.debug("cloudflare-dns-failover: could not pull zoneid")
        return False

    for item in result:
        logger.debug("cloudflare-dns-failover: Working on Redis item " + item)
        redis_data = json.loads(item)
        redis_data.pop("id", None)
        readd = cloudflare.add_rec(redata['data']['email'],
                                   redata['data']['apikey'],
                                   zoneid,
                                   logger,
                                   redis_data)
        if readd:
            result = r_server.srem("cloudflare-dns-failover:%s:%s" %
                                   (jdata['cid'], redata['id']), item)
            logger.debug("cloudflare-dns-failover: Re-added record %s" % item)
            readded = readded + 1
        else:
            logger.debug("cloudflare-dns-failover: Could not re-add record %s" % item)
    if readded > 0:
        return True
    else:
        return None

def run_reaction(redata, jdata, logger, r_server):
    ''' This method performs the heavy lifting '''
    removed = 0
    zoneid = cloudflare.get_zoneid(redata['data']['email'],
                                   redata['data']['apikey'],
                                   redata['data']['domain'],
                                   logger)
    if zoneid is None:
        logger.debug("cloudflare-dns-failover: could not pull zoneid")
        return False
    rec_data = {}
    if redata['data']['rec_name']:
        rec_data = {'name' : redata['data']['rec_name']}
    recs = cloudflare.get_recs(redata['data']['email'],
                               redata['data']['apikey'],
                               zoneid,
                               logger,
                               page=1,
                               search=rec_data)
    logger.debug("cloudflare-dns-failover: got records " + json.dumps(recs))
    if len(recs) < 1:
        logger.debug("cloudflare-dns-failover: could not pull records for domain %s" %
                     redata['data']['domain'])
        return False
    names = {}
    queued = {}
    for rec in recs.keys():
        name = recs[rec]['name'] + "-" + recs[rec]['type']
        if name in names:
            names[name].append(rec)
        else:
            names[name] = [rec]
        if (name in queued and
                recs[rec]['content'] == redata['data']['content']):
            queued[name].append(rec)
        elif recs[rec]['content'] == redata['data']['content']:
            queued[name] = [rec]

    for name in names.keys():
        if len(names[name]) > 1 and name in queued:
            for item in queued[name]:
                result = cloudflare.del_rec(redata['data']['email'],
                                            redata['data']['apikey'],
                                            zoneid,
                                            logger,
                                            item)
                logger.debug("cloudflare-dns-failover: Deleted record id %s" % item)
                if result:
                    removed = removed + 1
                    redis_key = "cloudflare-dns-failover:%s:%s" % (jdata['cid'],
                                                                   redata['id'],)
                    rec_json = json.dumps(recs[item])
                    try:
                        r_server.sadd(redis_key, rec_json)
                    except:
                        logger.debug("cloudflare-dns-failover: Could not add "
                                     " record to redis %s" % item)
                else:
                    logger.debug("cloudflare-dns-failover: Delete request "
                                 "of record id %s failed" % item)
    if removed == 0:
        return None
    else:
        return True
