######################################################################
# Cloud Routes Web Application
# -------------------------------------------------------------------
# Reaction Class
######################################################################

import rethinkdb as r


class Reaction(object):

    def __init__(self, rid=None):
        ''' Create a reaction object and set attributes as None for now '''
        self.rid = rid
        self.name = None
        self.rtype = None
        self.uid = None
        self.trigger = None
        self.lastrun = None
        self.frequency = None
        self.data = {}

    def createReaction(self, rdb):
        ''' This will create a reaction with the supplied information '''
        reactdata = {
            'name': self.name,
            'rtype': self.rtype,
            'uid': self.uid,
            'trigger': self.trigger,
            'frequency': self.frequency,
            'lastrun': 0,
            'data': self.data}
        if self.exists(reactdata['name'], reactdata['uid'], rdb):
            return 'exists'
        else:
            results = r.table('reactions').insert(reactdata).run(rdb)
            if results['inserted'] == 1:
                qdata = {}
                qdata['item'] = reactdata
                qdata['action'] = 'create'
                qdata['type'] = 'reaction'
                qdata['item']['rid'] = results['generated_keys'][0]
                q1 = r.table('dc1queue').insert(qdata).run(rdb)
                q2 = r.table('dc2queue').insert(qdata).run(rdb)
                return results['generated_keys'][0]
            else:
                return False

    def editReaction(self, rdb):
        ''' This will edit a reaction with the supplied information '''
        reactdata = {
            'name': self.name,
            'rtype': self.rtype,
            'uid': self.uid,
            'trigger': self.trigger,
            'frequency': self.frequency,
            'lastrun': self.lastrun,
            'data': self.data}
        results = r.table('reactions').get(self.rid).update(reactdata).run(rdb)
        if results['replaced'] == 1:
            qdata = {}
            qdata['item'] = reactdata
            qdata['action'] = 'edit'
            qdata['type'] = 'reaction'
            qdata['item']['rid'] = self.rid
            q1 = r.table('dc1queue').insert(qdata).run(rdb)
            q2 = r.table('dc2queue').insert(qdata).run(rdb)
            return "edit true"
        else:
            return "edit failed"

    def deleteReaction(self, uid, rid, rdb):
        ''' This will delete a specified reaction '''
        reaction = r.table('reactions').get(rid).run(rdb)
        if reaction['uid'] == uid:
            delete = r.table('reactions').get(rid).delete().run(rdb)
            if delete['deleted'] == 1:
                qdata = {}
                qdata['item'] = reaction
                qdata['action'] = 'delete'
                qdata['type'] = 'reaction'
                qdata['item']['rid'] = rid
                q1 = r.table('dc1queue').insert(qdata).run(rdb)
                q2 = r.table('dc2queue').insert(qdata).run(rdb)
                return True
            else:
                return False
        else:
            return False

    def exists(self, name, uid, rdb):
        '''
        This will check to see if the
        specified reactions already exists or not
        '''
        result = r.table('reactions').filter(
            {'name': name, 'uid': uid}).count().run(rdb)
        if result >= 1:
            return True
        else:
            return False

    def getRID(self, searchstring, rdb):
        ''' This will lookup a reaction by name and uid and return the rid '''
        strings = searchstring.split(":")
        result = r.table('reactions').filter(
            {'name': strings[0], 'uid': strings[1]}).run(rdb)
        xdata = {}
        for x in result:
            key = '%s:$s' % (x['name'], x['uid'])
            xdata[key] = x['id']
        return xdata[searchstring]

    def get(self, method, lookup, rdb):
        '''
        This will return a reactions
        information based on the data provided
        '''
        if method == 'rid':
            rid = lookup
        else:
            rid = self.getRID(lookup, rdb)
        results = r.table('reactions').get(rid).run(rdb)
        if results:
            self.rid = rid
            self.name = results['name']
            self.rtype = results['rtype']
            self.uid = results['uid']
            self.trigger = results['trigger']
            self.frequency = results['frequency']
            self.lastrun = results['lastrun']
            self.data = results['data']
            return self
        else:
            return False

    def count(self, uid, rdb):
        ''' This will return the numerical count of reactions by user id '''
        result = r.table('reactions').filter({'uid': uid}).count().run(rdb)
        return result


if __name__ == '__main__':
    pass
