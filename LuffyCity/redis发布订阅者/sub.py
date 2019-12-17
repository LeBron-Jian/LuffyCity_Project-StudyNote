#_*_coding:utf-8_*_
import redis

conn = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

# 第一步  生成一个订阅者对象
pubsub = conn.pubsub()

# 第二步  订阅一个消息
pubsub.subscribe('james')

# 创建一个接受
while True:
    print("working ...")
    msg = pubsub.parse_response()
    print(msg)