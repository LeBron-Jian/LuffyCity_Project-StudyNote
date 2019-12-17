# _*_coding:utf-8_*_
import redis

pool = redis.ConnectionPool(host='127.0.0.1',
                            port=6397,
                            decode_responses=True,
                            max_connections=10)

conn = redis.Redis(connection_pool=pool)

ret = conn.get('n1')
print(ret)