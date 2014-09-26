######################################################################
## Cloud Routes Web Application
## -------------------------------------------------------------------
## Datadog Monitor API modules
######################################################################

import json

def webCheck(request, monitor, cid, atype, rdb):
  ''' Process the webbased api call '''
  replydata = { 
    'headers': { 'Content-type' : 'application/json' }
    }
  rdata = {}
  jdata = request.json
   
  ## Delete the Monitor
  monitor.get(cid, rdb)
  if jdata['check_key'] == monitor.url and atype == monitor.ctype:
    if "Triggered" in jdata['title']:
      monitor.healthcheck = "failed"
      result = monitor.webCheck(rdb)
      if result:
        rdata['result'] = "success"
      else:  
        rdata['result'] = "failed"
    elif "No data" in jdata['title']:
      monitor.healthcheck = "failed"
      result = monitor.webCheck(rdb)
      if result:
        rdata['result'] = "success"
      else:  
        rdata['result'] = "failed"
    elif "Recovered" in jdata['title']:
      monitor.healthcheck = "healthy"
      result = monitor.webCheck(rdb)
      if result:
        rdata['result'] = "success"
      else:  
        rdata['result'] = "failed"
    else:
      rdata['result'] = "unknown request"
  else:
    rdata['result'] = "invalid key"

  replydata['data'] = json.dumps(rdata)
  
  return replydata

