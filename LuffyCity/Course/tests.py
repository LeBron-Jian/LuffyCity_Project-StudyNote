from django.test import TestCase
import redis

# Create your tests here.


conn = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

conn.set("n1", "v1")
# 下面将key的name 改为  k2 了。
conn.hset('n2', 'k2', 'v2')

ret1 = conn.get('n1')
ret2 = conn.hget('n2', 'k2')

print(ret1)
print(ret2)

'''
decode_responses=False
b'v1'
b'v2'
decode_responses=True
v1
v2
'''