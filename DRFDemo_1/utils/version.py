#_*_coding:utf-8_*_
# 框架给我们提供了很多版本控制类
from rest_framework import versioning

class MyVersion(object):
    # determine_version()这个方法返回的就是版本号
    def determine_version(self, request, *args, **kwargs):
        # 返回值  给了request.version
        # 返回版本号，
        # 版本号携带在过滤条件  xxxx?version = v1
        version = request.query_params.get("version", 'v1')
        return version