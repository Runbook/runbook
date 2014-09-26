######################################################################
## Cloud Routes Web Application
## -------------------------------------------------------------------
## Domains Class
######################################################################

import rethinkdb as r

class Domain(object):

  def __init__(self, did=None):
    ''' Create a domain object and set attributes as None for now '''
    self.did = did
    self.domain = None
    self.apikey = None
    self.failover = None
    self.uid = None
    self.email = None


  def createDomain(self, domaindata, rdb):
    ''' This will create a domain with the supplied domain information '''
    if self.exists(domaindata['domain'], rdb):
      return 'exists'
    else:
      results = r.table('domains').insert(domaindata).run(rdb)
      if results['inserted'] == 1:
        return results['generated_keys'][0]
      else:
        return False


  def deleteDomain(self, uid, did, rdb):
    ''' This will delete a specified domain id '''
    check = r.table('domains').get(did).run(rdb)
    if check['uid']:
      delete = r.table('domains').get(did).delete().run(rdb)
      if delete['deleted'] == 1:
        return True
      else:
        return False
    else:
      return False


  def exists(self, domain, rdb):
    ''' This will check to see if a domain with this name already exists, across all users ''' 
    result = r.table('domains').filter({'domain': domain}).count().run(rdb)
    if result >= 1:
      return True
    else:
      return False


  def getDID(self, domain, rdb):
    ''' This will lookup a domain by the domain name and return the domain id '''
    result = r.table('domains').filter({'domain': domain}).run(rdb)
    xdata = {}
    for x in result:
      xdata[x['domain']] = x['did']
    return xdata[domain]


  def get(self, method, lookup, rdb):
    ''' This will return a domains information based on the data provided '''
    if method == 'did':
      did = lookup
    else:
      did = self.getDID(lookup, rdb)
    results = r.table('domain').get(did).run(rdb)
    if results:
      self.did = did
      self.domain = results['domain']
      self.apikey = results['apikey']
      self.failover = results['failover']
      self.uid = results['uid']
      self.email = results['email']
      return self
    else:
      return False


  def getMonitors(self, did, rdb):
    ''' This will lookup and return all of the monitors available for this domain '''
    results = r.table('monitors').filter({'did': did}).run(rdb)
    xdata = {}
    for x in results:
      if x['id']:
        xdata[x['id']] = x
    return xdata


if __name__ == '__main__':
  pass
