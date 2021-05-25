# Simple Redis OSS Sentinel via Docker Compose

[Redis Sentinel is a watchdog for Redis OSS](https://redis.io/topics/sentinel)

* docker-compose to launch everything
* will start main/master --> replica instances
* will start up three redis instances with a redis sentinel config (3 processes for quorum)
* will allow you to see how the sentinel failover works

## Main/Replica Instances

These are in the docker-compose and should be familiar if you have run Redis via docker before.  The main/master is going to expose the default 6379 listen port. The slave/replica is going to use a custom command to make it a replica.

```
command: redis-server --slaveof redis-master 6379
```

## Sentinels

There is a folder called “redis-sentinel” which has three files to build the sentinel containers based on the standard Redis docker image but adding a custom entry point and sentinel (template) config.  The entrypoint script updates it's config with the Dockerfile environment variables and then starts Redis with the sentinel configuration and switch.

Using the docker network the sentinels can easily connect to the master and monitor whether it is still alive.

You can dig into the Dockerfile, sentinel-entrypoint.sh and the sentinel.conf to learn more.

## Using

```
docker-compose up
```

In another terminal tab/window pause the redis-main container you can run sentinel commands to verify things are working.

**discover master**
```
docker-compose exec redis-sentinel-1 redis-cli -p 26379 sentinel master rmain
```

**discover sentinels**
```
docker-compose exec redis-sentinel-1 redis-cli -p 26379 sentinel sentinels rmain
```

**discover replicas**
```
docker-compose exec redis-sentinel-1 redis-cli -p 26379 sentinel replicas rmain
```

**failover**
```
docker-compose pause redis-main 
```

View the logs in the main docker-compose window/tab to see the failover occur.  Check the state via redis-cli...

```
docker-compose exec redis-sentinel-1 redis-cli -p 26379 sentinel master rmain
```

Recover the container

```
docker-compose unpause redis-main 
```

Sentinel instances should automatically detect that the master instance is reachable again. Check the state via redis-cli...

```
docker-compose exec redis-sentinel-1 redis-cli -p 26379 sentinel master rmain
```


## Python Client Test Container

This is provided to play around with how discovery would work within an actual app and how it would use sentinel.

Since the master, replica and sentinels are within the docker network to properly test you will need to be able to have a client connect within that network.  There is one additional container started that is part of that same network with a source file mapped in to be able to run tests.

NOTE: You must run the command to create the cluster first before using the python client.

**source**:
You can put your own python code in *app* or just extend the basic exmaple already included:
`app/test.py`

**testing**  
The *app* directory is mapped to */usr/local/app* to run the test.py script you execute:

```
docker-compose exec app python /usr/local/app/test.py
```

**other languages**  
If you don't want to use python... you could start up another container with your source and language of choice.  Just make sure it's on the same docker network: *redis-oss-cluster_redissentinelnet* and you are connecting your client to the 10. IP like the test.py does.

## References (aka stole from...)

- https://www.developers-notebook.com/development/using-redis-sentinel-with-docker-compose/
