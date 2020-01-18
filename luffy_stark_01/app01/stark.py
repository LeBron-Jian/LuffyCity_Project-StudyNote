# _*_coding:utf-8_*_
from stark.service.v1 import site, StarkHandler
from app01 import models
from django.conf.urls import url
from django.shortcuts import HttpResponse


class DepartHandler(StarkHandler):
    def extra_urls(self):
        '''
        额外的增加url
        :return:
        '''
        return [
            url(r'^detail/(\d+)/$', self.detail_view)
        ]
    def detail_view(self):
        return HttpResponse("详细页面")


class UserInfoHandler(StarkHandler):
    def get_urls(self):
        '''
        修改url
        :return:
        '''
        patterns = [
            url(r'^list/$', self.change_view),
            url(r'^add/$', self.add_view),
        ]
        return patterns


site.register(models.UserInfo, UserInfoHandler)
# site.register(models.UserInfo, prev='private')
# site.register(models.UserInfo, prev='public')

# site.register(models.Depart, DepartHandler, prev='dba' )
site.register(models.Depart,)
