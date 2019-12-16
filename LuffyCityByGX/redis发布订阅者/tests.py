from django.test import TestCase
import redis
# Create your tests here.

conn = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)

conn.set("n1", "v1")
# conn.hset("n2", "k2", "v2")

# redis = {n2: {k2: v2}}

# ret1 = conn.get("n1")
# ret2 = conn.hget("n2", "k2")
# print(ret1)
# print(ret2)

conn.hset("n2", "k2", "v2")
conn.hmset("n3", {"k3": "v3", "k4": "v4"})


ret3 = conn.hget("n3", "k3")
ret4 = conn.hget("n3", "k4")
ret5 = conn.hgetall("n3")
ret6 = conn.get("xxxx")
print(ret6)

# print(ret3)
# print(ret4)
# print(ret5)

