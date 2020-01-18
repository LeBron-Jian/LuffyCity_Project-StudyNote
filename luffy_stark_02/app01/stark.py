# _*_coding:utf-8_*_
from stark.service.v1 import site, StarkHandler
from app01 import models
from django.urls import reverse
from django.conf.urls import url
from django.shortcuts import HttpResponse
from django.utils.safestring import mark_safe
from stark.service.v1 import site, StarkHandler, get_choice_text, Option


class DepartHandler(StarkHandler):
    # 优先执行这里的list_display，如果这里没有，则去父类里面找
    list_display = [StarkHandler.display_checkbox, 'id', 'title', StarkHandler.display_edit, StarkHandler.display_del]
    # pass
    has_add_btn = True
    search_list = ['title__contains', ]

    action_list = [StarkHandler.action_multi_delete, ]


class UserInfoHandler(StarkHandler):

    # def display_gender(self, obj=None, is_header=None):
    #     if is_header:
    #         return "性别"
    #     return obj.get_gender_display
    #
    # def display_classes(self, obj=None, is_header=None):
    #     if is_header:
    #         return "班级"
    #
    #     return obj.get_classes_display

    # 定制页面显示的列，我这里定义几个，则页面显示几个列
    list_display = [StarkHandler.display_checkbox,
                    'name', 'age', 'email',
                    get_choice_text('性别', 'gender'),
                    get_choice_text('班级', 'classes'),
                    StarkHandler.display_edit,
                    StarkHandler.display_del]

    # def get_list_display(self):
    #     return ['name', 'age', 'email', 'depart']

    has_add_btn = True

    order_list = ['id']
    search_list = ['name__contains']
    action_list = [StarkHandler.action_multi_delete, ]
    search_group = [
        Option('gender', is_multi=True),
        Option('depart', db_condition={'id__gt': 0}),
    ]

site.register(models.Depart, DepartHandler)

site.register(models.UserInfo, UserInfoHandler)
