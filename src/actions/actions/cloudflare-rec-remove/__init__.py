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
    # Check for Trigger
    if redata['trigger'] > jdata['failcount']:
        run = False

    # Check for lastrun
    checktime = time.time() - float(redata['lastrun'])
    if checktime < redata['frequency']:
        run = False

    if redata['data']['call_on'] not in jdata['check']['status']:
        run = False

    if run:
        return run_reaction(redata, jdata, logger, r_server)
    else:
        return None

def run_reaction(redata, jdata, logger, r_server):
    ''' This method performs the heavy lifting '''
    rec_data = {
        'type' : redata['data']['rec_type'],
        'content' : redata['data']['content']
    }
    if redata['data']['rec_name']:
        rec_data['name'] = redata['data']['rec_name']
    zoneid = cloudflare.get_zoneid(redata['data']['email'],
                                   redata['data']['apikey'],
                                   redata['data']['domain'],
                                   logger)
    if zoneid is not None:
        check = cloudflare.get_recs(redata['data']['email'],
                                    redata['data']['apikey'],
                                    zoneid,
                                    logger,
                                    page=1,
                                    search=rec_data)
        logger.debug("cloudflare-rec-remove: Got Records " + json.dumps(check))
        removed = 0
        for key in check.keys():
            logger.debug("cloudflare-rec-remove: Removing record id %s" % key)
            try:
                result = cloudflare.del_rec(redata['data']['email'],
                                               redata['data']['apikey'],
                                               zoneid,
                                               logger,
                                               key)
                if result is False:
                    logger.debug("cloudflare-rec-remove: Delete request of record id %s failed" % key)
                    return False
                else:
                    removed = removed + 1
            except:
                logger.debug("cloudflare-rec-remove: Calling delete record" +
                             " failed for id %s" % key)
                return False
        if removed == 0:
            return None
        else:
            return True
    else:
        logger.debug("cloudflare-rec-remove: Could not pull zone id for domain " +
                     redata['data']['domain'] + " for monitor  " + redata['id'])
        return False
