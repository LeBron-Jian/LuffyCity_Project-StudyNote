# _*_coding:utf-8_*_
from stark.service.v1 import site, StarkHandler
from app02 import models
from django.shortcuts import HttpResponse


class HostHandler(StarkHandler):
    pass


site.register(models.Host, HostHandler)


class RoleHandler(StarkHandler):
    pass


site.register(models.Role, RoleHandler)
