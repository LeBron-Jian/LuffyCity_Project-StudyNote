from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
import uuid
from .models import User


class DemoView(APIView):
    def get(self, request):
        return Response("认证Demo")

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        pwd = request.data.get('pwd')
        # 登录成功，生成一个token，会把token给你返回
        token = uuid.uuid4()
        User.objects.create(username=username, pwd=pwd, token=token)
        return Response("创建测试数据成功")

from utils.auth import MyAuth
from utils.permission import MyPermission
from utils.throttle import MyThrottle

class TestView(APIView):
    authentication_classes = [MyAuth, ]
    permission_classes = [MyPermission, ]
    throttle_classes = [MyThrottle, ]


    def get(self, request):
        print(request.auth)
        print(request.user)
        return Response("认证测试")

