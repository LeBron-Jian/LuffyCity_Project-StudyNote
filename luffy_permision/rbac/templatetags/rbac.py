# _*_coding:utf-8_*_
from django.template import Library
from django.conf import settings
from collections import OrderedDict
from django.shortcuts import render, redirect, reverse
from rbac.service import urls

import re

register = Library()


@register.inclusion_tag('rbac/static_menu.html')
def static_menu(request):
    '''
    创建一级菜单
    :param request:
    :return:
    '''
    menu_list = request.session[settings.MENU_SESSION_KEY]
    return {'menu_list': menu_list}


@register.inclusion_tag('rbac/multi_menu.html')
def multi_menu(request):
    '''
    创建2级菜单
    :param request:
    :return:
    '''
    menu_dict = request.session[settings.MENU_SESSION_KEY]
    print(request.current_selected_permission, type(request.current_selected_permission))

    # 对字典的key进行排序
    key_list = sorted(menu_dict)

    # 空的有序字典
    ordered_dict = OrderedDict()

    for key in key_list:
        val = menu_dict[key]
        # 默认给其加了一个hide属性，隐藏
        # val['class'] = 'hide'

        for per in val['children']:
            # regex = "^%s$" % (per['url'],)
            # if re.match(regex, request.path_info):
            if per['id'] == request.current_selected_permission:
                per['class'] = 'active'
                val['class'] = ''
        ordered_dict[key] = val

    return {'menu_dict': ordered_dict}


@register.inclusion_tag('rbac/breadcrumb.html')
def breadcrumb(request):
    return {'record_list': request.breadcrumb}

@register.filter
def has_permission(request, name):
    '''
    判断是否有权限
    最多有两个参数，第一个参数放在管道符前面。
    :param request:
    :param name:
    :return:
    '''
    if name in request.session[settings.PERMISSION_SESSION_KEY]:
        return True

@register.simple_tag
def memory_url(request, name, *args, **kwargs):
    '''
    生成带有原搜索条件的url，替代了模板中的url
    :param request:
    :param name:
    :return:
    '''
    return urls.memory_url(request, name, *args, **kwargs)
    # basic_url = reverse(name)
    # # 当前URL中无参数
    # if not request.GTE:
    #     return basic_url
    #
    # # 原来的搜索条件
    # # old_params = request.GET.urlencode()  # mid=2&age=99
    # # tpl = "%s?_filter=%s"%(basic_url, old_params)
    # # 如果这样拼接了 就会出现 /menu/add/?_filter=mid=2&age=99
    # # 这是什么问题呢？就是转义的问题
    #
    # # 所以我们这样做：
    # # 特殊的字典，实现的功能就是转义
    # from django.http import QueryDict
    # query_dict = QueryDict(mutable=True)
    # query_dict['_filter'] = request.GET.urlencode()
    # return "%s?%s"%(basic_url, query_dict.urlencode())