from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse

# Create your views here.

class DemoView(APIView):
    def get(self, request):
        res = 'handlerResponse("跨域测试")'
        # return Response(res)
        return HttpResponse(res)

    def put(self, request):
        return Response("put接口测试")

    def post(self, request):
        return Response("post 接口测试")


