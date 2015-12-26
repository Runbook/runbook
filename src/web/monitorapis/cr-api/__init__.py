######################################################################
# Cloud Routes Web Application
# -------------------------------------------------------------------
# CloudRoutes Monitor API modules
######################################################################

import json
from web import app


def webCheck(request, monitor, urldata, rdb):
    ''' Process the webbased api call '''
    replydata = {
        'headers': {'Content-type': 'application/json'}
    }
    rdata = {}
    jdata = request.json
    if jdata is None:
        jdata = urldata.copy()

    # Adding this because i'm lazy and didn't feel like modifying all the
    # references
    cid = urldata['cid']
    atype = urldata['atype']

    # Process API Request
    app.logger.debug("cr-api: looking up monitor id %s" % cid)
    monitor.get(cid, rdb)
    app.logger.info("cr-api: Monitor %s is - %s" % (cid, monitor.name))
    if jdata['check_key'] == monitor.url:
        app.logger.info("cr-api: monitor %s check_key is valid" % cid)
        if jdata['action'] == "false" or jdata['action'] == "failed":
            monitor.healthcheck = "false"
            result = monitor.webCheck(rdb)
            if result:
                app.logger.info("cr-api: change of webCheck for \
                      monitor {0} was successful".format(cid))
                rdata['result'] = "success"
            else:
                app.logger.info("cr-api: could not set webCheck for monitor %s" % cid)
                rdata['result'] = "failed"
        elif jdata['action'] == "true" or jdata['action'] == "healthy":
            monitor.healthcheck = "true"
            result = monitor.webCheck(rdb)
            if result:
                app.logger.info("cr-api: change of webCheck for \
                      monitor {0} was successful".format(cid))
                rdata['result'] = "success"
            else:
                app.logger.info("cr-api: could not set webCheck for monitor %s" % cid)
                rdata['result'] = "failed"
        elif jdata['action'] == "status":
            rdata['result'] = "success"
            if monitor.status == "false":
                rdata['status'] = "failed"
            elif monitor.status == "true":
                rdata['status'] = "healthy"
            else:
                rdata['status'] = monitor.status
            rdata['failcount'] = monitor.failcount
        else:
            app.logger.info("cr-api: Got an unknown action %s" % jdata['action'])
            rdata['result'] = "unkown action"
    else:
        app.logger.info("cr-api: monitor check_key is invalid")
        rdata['result'] = "invalid key"

    replydata['data'] = json.dumps(rdata)
    app.logger.debug("Returning API results: {0}".format(replydata['data']))

    return replydata
