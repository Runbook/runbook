import rethinkdb as r
conn = r.connect('localhost', 28015)

r.db('rethinkdb').table('cluster_config').get('auth').update(
    {'auth_key': 'cloudroutes'}
).run(conn)
