from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from SerDemo.models import Book
from SerDemo.serializers import BookSerializer

# Create your views here.
from rest_framework import pagination
from utils.pagination import MyPagination


class BookView1(APIView):

    def get(self, request):
        queryset = Book.objects.all()
        # 1,实例化分页器对象
        page_obj = MyPagination()
        # 2，调用分页方法去分页 queryset
        page_queryset = page_obj.paginate_queryset(queryset, request, view=self)
        # 3，把分页好的数据序列化返回
        # 4，带上上一页下一页的连接响应

        ser_obj = BookSerializer(queryset, many=True)

        return page_obj.get_paginated_response(ser_obj.data)


from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin


class BookView(GenericAPIView, ListModelMixin):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # 下面引入自己的分页器
    pagination_class = MyPagination

    def get(self, request):
        return self.list(request)
