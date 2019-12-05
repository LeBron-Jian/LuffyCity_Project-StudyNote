# _*_coding:utf-8_*_
from rest_framework.pagination import PageNumberPagination


class MyPagination1(PageNumberPagination):
    page_size = 1
    page_query_param = 'page'
    page_size_query_param = 'size'
    max_page_size = 3


from rest_framework.pagination import LimitOffsetPagination


class MyPagination2(LimitOffsetPagination):
    default_limit = 1
    limit_query_param = 'limit'
    offset_query_param = 'offset'  # 第几条数据
    max_limit = 3

from rest_framework.pagination import CursorPagination


class MyPagination(CursorPagination):
    cursor_query_param = 'cursor'
    page_size = 2
    # 排序，以id的倒序排序
    ordering = '-id'

