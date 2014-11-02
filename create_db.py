import rethinkdb as r
from rethinkdb.errors import RqlDriverError, RqlRuntimeError

# todo: I don't know another easy way to parse a flask config
execfile("instance/crweb.cfg")
# now params like DBHOST, DATABASE, DBAUTHKEY are global variables


def connect():
    try:
        conn = r.connect(DBHOST, 28015, auth_key=DBAUTHKEY).repl()
        r.db_create(DATABASE).run(conn)
        r.db(DATABASE).table_create('monitors').run(conn)
        r.db(DATABASE).table_create('reactions').run(conn)
        r.db(DATABASE).table_create('users').run(conn)
        r.db(DATABASE).table_create('history').run(conn)
        r.db(DATABASE).table_create('events').run(conn)
        r.db(DATABASE).table_create('subscription_history').run(conn)
        r.db(DATABASE).table_create('dc1queue').run(conn)
        r.db(DATABASE).table_create('dc2queue').run(conn)
        return "Done!"
    except RqlDriverError, e:
        return e
    except RqlRuntimeError, e:
        return e


print connect()


#######################
### Database Tables ###
#######################

"""
monitors - Stores monitors
reactions - Stores reactions
users - Stores user data
history - Stores historical tracking for monitors and reactions
events - Stores unique events for monitors
subscription_history - Stores subscription history for tracking signups
dc1queue - Queue for monitors and reactions in datacenter 1
dc2queue - Queue for monitors and reactions in datacenter 2
"""
