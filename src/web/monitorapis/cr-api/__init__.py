######################################################################
# Cloud Routes Web Application
# -------------------------------------------------------------------
# CloudRoutes Monitor API modules
######################################################################

import json


def webCheck(request, monitor, urldata, rdb):
    ''' Process the webbased api call '''
    replydata = {
        'headers': {'Content-type': 'application/json'}
    }
    rdata = {}
    jdata = request.json

    # Adding this because i'm lazy and didn't feel like modifying all the
    # references
    cid = urldata['cid']
    atype = urldata['atype']

    # Process API Request
    print("cr-api: looking up monitor id %s") % cid
    monitor.get(cid, rdb)
    print("cr-api: Monitor %s is - %s") % (cid, monitor.name)
    if jdata['check_key'] == monitor.url:
        print("cr-api: monitor %s check_key is valid") % cid
        if jdata['action'] == "false" or jdata['action'] == "failed":
            monitor.healthcheck = "false"
            result = monitor.webCheck(rdb)
            if result:
                print("cr-api: change of webCheck for monitor %s was successful") % cid
                rdata['result'] = "success"
            else:
                print("cr-api: could not set webCheck for monitor %s") % cid
                rdata['result'] = "failed"
        elif jdata['action'] == "true" or jdata['action'] == "healthy":
            monitor.healthcheck = "true"
            result = monitor.webCheck(rdb)
            if result:
                print("cr-api: change of webCheck for monitor %s was successful") % cid
                rdata['result'] = "success"
            else:
                print("cr-api: could not set webCheck for monitor %s") % cid
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
            print("cr-api: Got an unknown action %s") % jdata['action']
            rdata['result'] = "unkown action"
    else:
        print("cr-api: monitor check_key is invalid")
        rdata['result'] = "invalid key"

    replydata['data'] = json.dumps(rdata)

    return replydata
