######################################################################
# Cloud Routes Web Application
# -------------------------------------------------------------------
# Users Class
######################################################################

from werkzeug.security import generate_password_hash, check_password_hash
import hashlib
import rethinkdb as r
import time
from monitors import Monitor
from reactions import Reaction


class User(object):

    def __init__(self, uid=None):
        ''' Initialize the User Class '''
        self.uid = uid
        self.email = None
        self.username = None
        self.status = None
        self.company = None
        self.contact = None
        self.domains = {}
        self.reactions = {}
        self.monitors = {}
        self.acttype = None
        self.stripe = None
        self.stripeid = None
        self.subplans = 2
        self.subscription = 'Free'
        self.payments = 'Stripe'
        self.subscribed_to_newsletter = False
        self.confirmed = False
        self.confirmed_on = None
        self.upgraded = False
        self.monitorCount = None
        self.reactionCount = None
        self.config = None

    def createUser(self, userdata, rdb):
        '''
        Given-

        userdata = {
            "username": "foo",
            "password": "foo_password",
            "email": "foo@bar.com",
            "company": "foobar",
            "contact": "foo@bar.com""
        }

        - create a new user in the RethinkDB database
        '''
        jsondata = {}
        jsondata['username'] = userdata['username']
        jsondata['password'] = self.createPass(userdata['password'])
        jsondata['email'] = userdata['email']
        jsondata['status'] = 'active'
        jsondata['company'] = userdata['company']
        jsondata['acttype'] = 'lite-v2'
        jsondata['contact'] = userdata['contact']
        jsondata['stripe'] = self.stripe
        jsondata['stripeid'] = self.stripeid
        jsondata['subplans'] = self.subplans
        jsondata['payments'] = self.payments
        jsondata['subscription'] = self.subscription
        jsondata['subscribed_to_newsletter'] = self.subscribed_to_newsletter
        jsondata['creation_time'] = time.time()
        jsondata['confirmed'] = False

        if self.is_active(userdata['username'], rdb):
            return 'exists'
        else:
            results = r.table('users').insert(jsondata).run(rdb)
            if results['inserted'] == 1:
                return results['generated_keys'][0]
            else:
                return False

    def saltPass(self, password):
        ''' Create a appsalt + user password hash (better than default) '''
        salty_pass = self.config['PASSWORD_SALT'] + password
        return hashlib.sha512(salty_pass).hexdigest()

        
    def createPass(self, password):
        ''' Create a salted hashed password '''
        password = self.saltPass(password)
        return generate_password_hash(password)

    def setPass(self, newpass, rdb):
        ''' Set a password in the database '''
        password = self.createPass(newpass)
        results = r.table('users').get(self.uid).update(
            {'password': password}).run(rdb)
        if results['replaced'] == 1:
            return True
        else:
            return False

    def getUID(self, username, rdb):
        ''' Lookup a users uid by username '''
        results = r.table('users').filter(
            r.row['username'] == username).run(rdb)
        xdata = {}
        for x in results:
            key = x['username']
            value = x['id']
            xdata[key] = value
        if username in xdata:
            return xdata[username]
        else:
            return False

    def get(self, method, lookup, rdb):
        ''' Lookup the user by the uid '''
        if method == 'uid':
            uid = lookup
        elif method == 'username':
            uid = self.getUID(lookup, rdb)
        results = r.table('users').get(uid).run(rdb)
        data = results
        if data:
            self.email = results['email']
            self.uid = results['id']
            self.username = results['username']
            self.status = results['status']
            self.company = results['company']
            self.contact = results['contact']
            self.acttype = results['acttype']
            self.stripeid = results['stripeid']
            self.stripe = results['stripe']
            self.subplans = results['subplans']
            self.payments = results['payments']
            self.subscription = results['subscription']
            self.creation_time = results['creation_time']
            self.confirmed = results['confirmed']
            ## Identify number of monitors and reactions
            monitor = Monitor()
            reaction = Reaction()
            self.monitorCount = monitor.count(self.uid, rdb)
            self.reactionCount = reaction.count(self.uid, rdb)
            return self
        else:
            return None

    def checkPass(self, password, rdb):
        ''' Check if the password supplied is valid '''
        results = r.table('users').get(self.uid).run(rdb)
        data = results
        if not data:
            return "No data found"
        else:
           if check_password_hash(data['password'], password):
              self.setPass(password, rdb)
              return True
           else:
              password = self.saltPass(password)
              return check_password_hash(data['password'], password)

    def is_active(self, username, rdb):
        ''' Check if a user exists or not '''
        count = r.table('users').filter(
            {'username': username}).count().run(rdb)
        if count >= 1:
            self.active = True
        else:
            self.active = False
        return self.active

    def is_confirmed(self, username, rdb):
        ''' Check if a user is confirmed or not '''
        results = r.table('users').filter({'username': username}).run(rdb)
        if results:
            return self.confirmed
        else:
            return "No data found"

    def getDomains(self, rdb):
        ''' Returns a list of domain id's that this user owns '''
        # Get Domains
        results = r.table('domains').filter({'uid': self.uid}).run(rdb)
        domains = {}
        for x in results:
            domains[x['id']] = x
        self.domains = domains
        return self.domains

    def getReactions(self, rdb):
        ''' Returns a list of reaction id's that this user owns '''
        # Get Reactions
        results = r.table('reactions').filter(
            {'uid': self.uid}).order_by('name').run(rdb)
        reactions = {}
        for x in results:
            reactions[x['id']] = x
        self.reactions = reactions
        return self.reactions

    def getMonitors(self, rdb):
        ''' Returns a list of monitor id's that this user owns '''
        # Get Monitors
        results = r.table('monitors').filter(
            {'uid': self.uid}).order_by('name').run(rdb)
        monitors = {}
        for x in results:
            monitors[x['id']] = x
        self.monitors = monitors
        return self.monitors

    def getEvents(self, rdb):
        ''' Returns a list of events from the events table for this user '''
        # Get Events
        results = r.table('events').filter({'uid': self.uid}).order_by(
            r.desc('time')).run(rdb)
        eventsbycid = {}
        for event in results:
            if event['cid'] in eventsbycid:
                eventsbycid[event['cid']].append(event)
            else:
                eventsbycid[event['cid']] = [ event ]
        return eventsbycid

    def setSubscription(self, rdb):
        '''
        This will set a users subscription
        to the specified subscription plan
        '''
        # Get User id
        results = r.table('users').get(self.uid).update(
            {
                'acttype': self.acttype,
                'stripeid': self.stripeid,
                'stripe': self.stripe,
                'subscription': self.subscription,
                'subplans': self.subplans
            }
        ).run(rdb)
        if results:
            loginfo = {}
            loginfo['type'] = "setSubscription"
            loginfo['uid'] = self.uid
            loginfo['acttype'] = self.acttype
            loginfo['subplans'] = self.subplans
            loginfo['subscription'] = self.subscription
            loginfo['time'] = time.time()
            logresult = r.table('subscription_history').insert(
                loginfo).run(rdb)
            return True
        else:
            return False


if __name__ == '__main__':  # pragma: no cover
    pass                    # pragma: no cover
