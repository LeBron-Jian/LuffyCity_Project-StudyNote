from django.shortcuts import render

# Create your views here.
from django.views import View
from django.http import HttpResponse
from django.core.handlers.wsgi import WSGIRequest
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.negotiation import DefaultContentNegotiation
from rest_framework import parsers

class DjangoView(View):
    def get(self, request):
        # 打印一下request的类型，到底是哪个类封装的
        print(type(request))
        '''
        Request
        request.get
        request.post
        '''
        return HttpResponse("Django的解析器测试")


class DRFView(APIView):
    # 如果在这里配置了解析器，那么这个视图只能解析JSON数据
    # 所以一般，我们不会配置解析器
    parser_classes = [parsers.JSONParser, ]

    def get(self, request):
        # request 是我们重新封装的request，是用Request封装的
        # request.data
        return Response("DRF解析器的测试")