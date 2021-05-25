from redis.sentinel import Sentinel

conf = {
    'sentinel': [('redis-sentinel-1', 26379), ('redis-sentinel-1', 26379), ('redis-sentinel-1', 26379)],
    'master_group_name': 'rmain',
    #Connect sentinel configuration
    'sentinel_conf': { 
        'socket_timeout': 3,
        'socket_keepalive': True,
    #    'password': 'w2opw723DaAp0rUc'
    },
    'connection_conf': {
        'socket_timeout': 3,
        'retry_on_timeout': True,
        'socket_keepalive': True,
        'max_connections': 5,
        'db': 0,
        #'password': 'w2opw723DaAp0rUc',
        'encoding': 'utf8'
    }
}
sentinel = Sentinel(conf['sentinel'],sentinel_kwargs=conf['sentinel_conf'],**conf['connection_conf'])
sentinel.discover_master(conf['master_group_name'])
print("sentinels output:")
print(sentinel.sentinels)
cli = sentinel.master_for(conf['master_group_name'])

cli.set('status', 'Redis master obtained through sentinel')
print(cli.get('status'))