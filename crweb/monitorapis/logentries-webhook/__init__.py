######################################################################
## Cloud Routes Web Application
## -------------------------------------------------------------------
## Datadog Monitor API modules
######################################################################

import json

def webCheck(request, monitor, urldata, rdb):
  ''' Process the webbased api call '''
  replydata = { 
    'headers': { 'Content-type' : 'application/json' }
    }
  rdata = {}
  if request.method == "POST" and "payload" in request.form:
    request_verify = True
  else:
    request_verify = False
   
  ## Monitor
  monitor.get(urldata['cid'], rdb)
  if urldata['check_key'] == monitor.url and urldata['atype'] == monitor.ctype:
    if urldata['action'] == "failed" or urldata['action'] == "healthy":
      monitor.healthcheck = urldata['action']
      result = monitor.webCheck(rdb)
      if result:
        rdata['result'] = "success"
      else:  
       rdata['result'] = "failed"
    else:
      rdata['result'] = "failed"
  else:
    rdata['result'] = "invalid key"

  replydata['data'] = json.dumps(rdata)
  
  return replydata

