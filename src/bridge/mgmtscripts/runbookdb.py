import yaml
import rethinkdb as r
from rethinkdb.errors import RqlDriverError


class RunbookDB(object):
    def __init__(self, configfile):
        with open(configfile, 'r') as cfh:
            self.config = yaml.safe_load(cfh)
    
    def connect(self):
        try:
            if self.config['rethink_authkey']:
                self.conn = r.connect(
                    host=self.config['rethink_host'], port=self.config['rethink_port'],
                    auth_key=self.config['rethink_authkey'], db=self.config['rethink_db']).repl()
            else:
                self.conn = r.connect(
                    host=self.config['rethink_host'], port=self.config['rethink_port'],
                    db=self.config['rethink_db']).repl()
                print "Connecting to RethinkDB"
            return self.conn
        except RqlDriverError:
            #This is acceptable at the moment since that's the normal behavior for every management script
            print "Cannot connect to rethinkdb, shutting down"
            sys.exit(1) 

    def close(self):
        self.conn.close()

