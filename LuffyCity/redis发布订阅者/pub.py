#_*_coding:utf-8_*_
import redis

conn = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

conn.publish('james', 'mvp')