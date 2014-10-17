import rethinkdb as r
from rethinkdb.errors import RqlDriverError, RqlRuntimeError


def connect():
    try:
        conn = r.connect("localhost", 28015).repl()
        r.db_create('crdb').run(conn)
        r.db('crdb').table_create('monitors').run(conn)
        r.db('crdb').table_create('reactions').run(conn)
        r.db('crdb').table_create('users').run(conn)
        r.db('crdb').table_create('history').run(conn)
        r.db('crdb').table_create('events').run(conn)
        r.db('crdb').table_create('subscription_history').run(conn)
        r.db('crdb').table_create('dc1queue').run(conn)
        r.db('crdb').table_create('dc2queue').run(conn)
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
