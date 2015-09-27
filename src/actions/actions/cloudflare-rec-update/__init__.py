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
        return run_reaction(redata, jdata, logger)
    else:
        return None


def run_reaction(redata, jdata, logger):
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
        logger.debug("cloudflare-rec-update: Got Records " + json.dumps(check))
        modified = 0
        for key in check.keys():
            logger.debug("cloudflare-rec-update: Replacing record id %s" % key)
            new_rec_data = {
                'id' : key,
                'zone_id': zoneid,
                'name' : check[key]['name'],
                'type' : redata['data']['new_rec_type'],
                'content' : redata['data']['new_content'],
            }
            try:
                result = cloudflare.update_rec(redata['data']['email'],
                                               redata['data']['apikey'],
                                               zoneid,
                                               logger,
                                               key,
                                               new_rec_data)
                if result is False:
                    logger.debug("cloudflare-rec-update: Replacing record id %s failed" % key)
                    return False
                else:
                    modified = modified + 1
            except:
                logger.debug("cloudflare-rec-update: Calling update record" +
                             " failed for id %s" % key)
                return False
        if modified == 0:
            return None
        else:
            return True
    else:
        logger.debug("cloudflare-rec-add: Could not pull zone id for domain " +
                     redata['data']['domain'] + " for monitor  " + redata['id'])
        return False
