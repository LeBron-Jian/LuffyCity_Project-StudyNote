from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from .models import Book, Publisher, Author
from django.core import serializers
import json

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BookSerializer

# Create your views here.
'''
大概book_lits就是下面的类型
book_list = [
    {
        "id": 1,
        'title': 'xxx',
        ......
    },
    {

    }
]
'''


class BookView1(View):
    # 第一版，使用values,JsonResponse实现序列化
    # def get(self, request):
    #     book_list = Book.objects.values('id', 'title', 'pub_time', 'publisher')
    #     book_list = list(book_list)
    #     # ret = json.dumps(book_list, ensure_ascii=False)
    #     # return HttpResponse(ret)
    #     # 我们发现JSONResponse是继承HTTPResponse的
    #     ret = []
    #     for book in book_list:
    #         publisher_id = book['publisher']
    #         publisher_obj = Publisher.objects.filter(id=publisher_id).first()
    #         book['publisher'] = {
    #             'id': publisher_id,
    #             'title': publisher_obj.title
    #
    #         }
    #         ret.append(book)
    #
    #     return JsonResponse(ret, safe=False,
    #                         json_dumps_params={'ensure_ascii': False})

    # 第二版，使用django serializers来更新
    def get(self, request):
        book_list = Book.objects.all()
        ret = serializers.serialize('json', book_list, ensure_ascii=False)
        return HttpResponse(ret)


class BookView2(APIView):
    def get(self, request):
        # book_obj = Book.objects.first()
        # ret = BookSerializer(book_obj)
        book_obj = Book.objects.all()
        ret = BookSerializer(book_obj, many=True)
        return Response(ret.data)

    def post(self, request):
        # 我们需要取到前端传来的数据
        # 在Django中我们会通过request.POST
        print(request.data)
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            # 如果验证通过，那么我们保存数据
            serializer.save()
            return Response(serializer.validated_data)
        else:
            return Response(serializer.errors)


class GenericAPIView(APIView):
    query_set = None
    serializer_class = None

    def get_queryset(self):
        return self.query_set

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)


# Mixin表示这个类时混合类，不能单独继承，单独继承没有任何意义
class ListModelMixin(object):
    # 把get()方法抽离出来
    def list(self, request):
        queryset = self.get_queryset()
        ret = self.get_serializer(queryset, many=True)
        return Response(ret.data)


class CreateModelMixin(object):
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # 如果验证通过，那么我们保存数据
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class RetrieveModelMixin(object):
    def retrieve(self, request, id):
        book_obj = self.get_queryset().filter(id=id).first()
        # ret = BookSerializer(book_obj)
        ret = self.get_serializer(book_obj)
        return Response(ret.data)


class UpdateModelMixin(object):
    def update(self, request, id):
        book_obj = self.get_queryset().filter(id=id).first()
        serializer = self.get_serializer(book_obj, data=request.data, partial=True)
        if serializer.is_valid():
            # 如果验证通过，那么我们保存数据
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class DestroyModelMixin(object):
    def destroy(self, request, id):
        book_obj = self.get_queryset().filter(id=id).first()
        book_obj.delete()
        return Response('删除完毕')


class ListCreateAPIView(GenericAPIView, ListModelMixin, CreateModelMixin):
    pass


class RetrieveUpdateDestoryAPIView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    pass


class BookView(ListCreateAPIView):
    # class BookView(GenericAPIView, ListModelMixin, CreateModelMixin):
    query_set = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request):
        # book_obj = Book.objects.all()
        # book_list = self.get_queryset()
        # ret = self.get_serializer(book_list, many=True)
        # return Response(ret.data)
        return self.list(request)

    def post(self, request):
        # 我们需要取到前端传来的数据
        # 在Django中我们会通过request.POST
        # print(request.data)
        # serializer = BookSerializer(data=request.data)
        # if serializer.is_valid():
        #     # 如果验证通过，那么我们保存数据
        #     serializer.save()
        #     return Response(serializer.validated_data)
        # else:
        #     return Response(serializer.errors)
        return self.create(request)


class BookEditView(RetrieveUpdateDestoryAPIView):
    # class BookEditView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    query_set = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, id):
        # book_obj = Book.objects.filter(id=id).first()
        # ret = BookSerializer(book_obj)
        # return Response(ret.data)
        return self.retrieve(request, id)

    def put(self, request, id):
        # book_obj = Book.objects.filter(id=id).first()
        # # partial=True 表示允许更新
        # serializer = BookSerializer(book_obj, data=request.data, partial=True)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.validated_data)
        # else:
        #     return Response(serializer.errors)
        return self.update(request, id)

    def delete(self, request, id):
        # book_obj = Book.objects.filter(id=id).first()
        # book_obj.delete()
        # return Response("")
        return self.destroy(request, id)


class ViewSetMixin111(object):
    # 我们需要重构as_view(）方法
    def as_view(self):
        '''
        按照我们参数指定的去匹配
        get ----》 list
        :return:
        '''


#  但是这个类不需要我们去写，框架已经为我们提供了
from rest_framework.viewsets import ViewSetMixin


class ModelViewSet1(ViewSetMixin, GenericAPIView, ListModelMixin, CreateModelMixin, RetrieveModelMixin,
                   UpdateModelMixin, DestroyModelMixin):
    pass


class BookModelViewSet1(ModelViewSet1):
    query_set = Book.objects.all()
    print(query_set)
    serializer_class = BookSerializer

    # get -- self.list

from rest_framework.viewsets import ModelViewSet


class BookModelViewSet(ModelViewSet):
    quert_set = Book.objects.all()
    serializer_class = BookSerializer


# from rest_framework import views
# from rest_framework import generics
# from rest_framework import mixins
# from rest_framework import viewsets
