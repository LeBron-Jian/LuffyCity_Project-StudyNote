# _*_coding:utf-8_*_
from rest_framework.throttling import BaseThrottle, SimpleRateThrottle
import time

VISIT_RECORD = {}


class MyThrottle1(BaseThrottle):

    def __init__(self):
        self.history = []

    def allow_request(self, request, view):
        # 实现限流的逻辑，如下：
        # 1，以IP限流
        # 2，访问列表  ——》这是一个字典，{IP： [time1, time2, time3]}

        # 生成访问列表后，首先1，我们获取请求的IP地址
        #               其次2，判断IP地址是否在访问列表中
        #                  ——如果不在，1：需要给访问列表添加访问时间 key  value
        #                  ——如果在，2：需要把这个IP的访问记录，把当前的时间加入到列表
        # 然后3，确保列表里最开始（最老的）的访问时间和最新的访问时间是否为1分钟——这里限流为1分钟
        # 其次4：得到列表长度，判断是否允许的次数，是否小于5
        ip = request.META.get("REMOTE_ADDR")  # 1
        now = time.time()  # 2
        if ip not in VISIT_RECORD:  # 2.1
            VISIT_RECORD[ip] = [now, ]
            return True
        history = VISIT_RECORD[ip]  # 2.2
        # 将最新的时间加入列表的前面，而不是后面，我们后面方便去pop
        history.insert(0, now)
        while history and history[0] - history[-1] > 60:  # 3
            history.pop()
        self.history = history
        if len(history) > 3:  # 4
            return False
        else:
            return True

        pass

    def wait(self):
        # 返回需要再等多久才能访问
        # 0 表示最新的时间，-1表示最老的时间
        time = 60 - (self.history[0] - self.history[-1])
        return time


class MyThrottle(SimpleRateThrottle):
    scope = 'WD'

    def get_cache_key(self, request, view):
        # 如果以IP地址作为限流返回IP地址
        key = self.get_ident(request)
        return key
