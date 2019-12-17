#_*_coding:utf-8_*_
import redis

POOL = redis.ConnectionPool(host='127.0.0.1',
                            port=6379,
                            decode_responses=True,
                            max_connections=10,)