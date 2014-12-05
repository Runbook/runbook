######################################################################
# Cloud Routes Web Application
# -------------------------------------------------------------------
# Monitors Class
######################################################################

import rethinkdb as r
from itsdangerous import URLSafeSerializer
import datetime


class Monitor(object):

    def __init__(self, cid=None, uid=None):
        ''' Create a health check object and set attributes as None for now '''
        self.cid = cid
        self.name = None
        self.ctype = None
        self.uid = None
        self.status = None
        self.failcount = None
        self.url = None
        self.healthcheck = None
        self.data = {}

    def genURL(self, cid, rdb):
        ''' This creates a safe url for monitors to send failures or success '''
        s = URLSafeSerializer(self.ctype)
        self.url = s.dumps([cid])
        urldata = {
            'url': self.url
        }
        results = r.table('monitors').get(cid).update(urldata).run(rdb)
        if results['replaced'] == 1:
            return True
        else:
            return False

    def createMonitor(self, rdb):
        '''
        This will create a health check with
        the supplied domain information
        '''
        mondata = {
            'name': self.name,
            'ctype': self.ctype,
            'uid': self.uid,
            'url': self.url,
            'failcount': 0,
            'status': self.status,
            'data': self.data}
        if self.exists(mondata['name'], mondata['uid'], rdb):
            return 'exists'
        else:
            mondata['status'] = 'queued'
            results = r.table('monitors').insert(mondata).run(rdb)
            if results['inserted'] == 1:
                qdata = {}
                qdata['item'] = mondata
                qdata['action'] = 'create'
                qdata['type'] = 'monitor'
                qdata['item']['cid'] = results['generated_keys'][0]
                self.cid = results['generated_keys'][0]
                urlchk = self.genURL(self.cid, rdb)
                if urlchk:
                    qdata['item']['url'] = self.url
                for dc in ["dc1queue", "dc2queue"]:
                    q1 = r.table(dc).insert(qdata).run(rdb)
                return results['generated_keys'][0]
            else:
                return False

    def editMonitor(self, rdb):
        ''' This will edit a health check with the supplied information '''
        mondata = {
            'name': self.name,
            'ctype': self.ctype,
            'uid': self.uid,
            'url': self.url,
            'failcount': 0,
            'status': self.status,
            'data': self.data}
        results = r.table('monitors').get(self.cid).update(mondata).run(rdb)
        if results['replaced'] == 1:
            qdata = {}
            qdata['item'] = mondata
            qdata['action'] = 'edit'
            qdata['type'] = 'monitor'
            qdata['item']['cid'] = self.cid
            for dc in ["dc1queue", "dc2queue"]:
                q1 = r.table(dc).insert(qdata).run(rdb)
            return True
        else:
            return False

    def deleteMonitor(self, uid, cid, rdb):
        ''' This will delete a specified health check '''
        check = r.table('monitors').get(cid).run(rdb)
        if check['uid'] == uid:
            delete = r.table('monitors').get(cid).delete().run(rdb)
            if delete['deleted'] == 1:
                qdata = {}
                qdata['item'] = check
                qdata['action'] = 'delete'
                qdata['type'] = 'monitor'
                qdata['item']['cid'] = cid
                for dc in ["dc1queue", "dc2queue"]:
                    q1 = r.table(dc).insert(qdata).run(rdb)
                return True
            else:
                return False
        else:
            return False

    def webCheck(self, rdb):
        ''' This will edit a health check with the supplied information '''
        mondata = {
            'name': self.name,
            'ctype': self.ctype,
            'uid': self.uid,
            'url': self.url,
            'data': self.data}
        qdata = {}
        qdata['item'] = mondata
        qdata['action'] = 'sink'
        qdata['type'] = 'monitor'
        qdata['item']['cid'] = self.cid
        qdata['item']['id'] = self.cid
        qdata['item']['check'] = {'status': self.healthcheck,
                                  'method': 'manual'}
        for dc in ["dc1queue", "dc2queue"]:
            q1 = r.table(dc).insert(qdata).run(rdb)
        return True

    def history(
        self, method=None, hid=None,
            time=None, start=None, limit=None, rdb=None):
        ''' This will pull a monitors history from rethinkDB '''
        retdata = False
        if method == "mon-history":
            retdata = []
            monitors = r.table('history').filter(
                (r.row['cid'] == self.cid) & (r.row['starttime'] >= time) & (r.row['type'] == "monitor")).order_by(
                r.desc('starttime')).pluck('starttime', 'id', 'cid', 'zone', 'status', 'failcount', 'method', 'name').skip(start).limit(limit).run(rdb)
            for mon in monitors:
                mon['starttime'] = datetime.datetime.fromtimestamp(
                    mon['starttime']).strftime('%Y-%m-%d %H:%M:%S')
                retdata.append(mon)
        elif method == "detail-history":
            retdata = []
            mon = r.table('history').get(hid).pluck(
                'starttime', 'cid', 'zone', 'status',
                'failcount', 'method', 'name').run(rdb)
            mon['reactions'] = []
            reactions = r.table('history').filter(
                (r.row['cid'] == self.cid) & (r.row['starttime'] == mon['starttime']) & (r.row['zone'] == mon['zone']) & (r.row['type'] == "reaction")).pluck('name', 'rstatus', 'time', 'starttime').run(rdb)
            for react in reactions:
                react['starttime'] = datetime.datetime.fromtimestamp(
                    react['starttime']).strftime('%Y-%m-%d %H:%M:%S')
                react['time'] = datetime.datetime.fromtimestamp(
                    react['time']).strftime('%Y-%m-%d %H:%M:%S')
                mon['reactions'].append(react)
            mon['starttime'] = datetime.datetime.fromtimestamp(
                mon['starttime']).strftime('%Y-%m-%d %H:%M:%S')
            retdata.append(mon)
        elif method == "count":
            retdata = r.table('history').filter(
                (r.row['cid'] == self.cid) & (r.row['starttime'] >= time) & (r.row['type'] == "monitor")).count().run(rdb)
        return retdata

    def exists(self, name, uid, rdb):
        '''
        This will check to see if the
        specified monitor already exists or not
        '''
        result = r.table('monitors').filter(
            {'name': name, 'uid': uid}).count().run(rdb)
        if result >= 1:
            return True
        else:
            return False

    def getCID(self, name, uid, rdb):
        ''' This will lookup a monitor by data + uid and return the check id '''
        result = r.table('monitors').filter(
            {'name': name, 'uid': uid}).run(rdb)
        cid = result[0]['cid']
        return cid

    def get(self, cid, rdb):
        ''' Get a monitor object by looking it up '''
        results = r.table('monitors').get(cid).run(rdb)
        if results:
            self.cid = cid
            self.name = results['name']
            self.ctype = results['ctype']
            self.uid = results['uid']
            self.url = results['url']
            self.failcount = results['failcount']
            self.data = results['data']
            self.status = results['status']
            return self
        else:
            return False

    def count(self, uid, rdb):
        ''' This will return the numerical count of monitors by user id '''
        result = r.table('monitors').filter({'uid': uid}).count().run(rdb)
        return result


if __name__ == '__main__':
    pass
