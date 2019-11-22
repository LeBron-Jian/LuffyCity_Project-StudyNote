# _*_coding:utf-8_*_

from django.urls import reverse
from django.http import QueryDict


def memory_url(request, name, *args, **kwargs):
    '''
    生成带有原搜索条件的url，替代了模板中的url
    :param request:
    :param name:
    :return:
    '''
    basic_url = reverse(name, args=args, kwargs=kwargs)
    # 当前URL中无参数
    if not request.GET:
        return basic_url

    query_dict = QueryDict(mutable=True)
    query_dict['_filter'] = request.GET.urlencode()
    return "%s?%s" % (basic_url, query_dict.urlencode())


def memory_reverse(request, name, *args, **kwargs):
    '''
    反向生成url
        1,在url中讲原来的搜索条件，如filter后的值
        2，reverse生成原来的URL，如/menu/list/
    :param request:
    :param name:
    :param args:
    :param kwargs:
    :return:
    '''
    url = reverse(name, args=args, kwargs=kwargs)
    origin_params = request.GET.get('_filter')
    if origin_params:
        url = '%s?%s' % (url, origin_params,)
    return url
