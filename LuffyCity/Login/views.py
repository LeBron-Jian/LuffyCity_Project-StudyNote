from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer
from utils.base_response import BaseResponse
from utils.redis_pool import POOL
from utils.my_auth import LoginAuth
from Course.models import Account
import redis
import uuid


# Create your views here.

class RegisterView(APIView):

    def post(self, request):
        res = BaseResponse()
        # 用序列化器做校验
        ser_obj = RegisterSerializer(data=request.data)
        if ser_obj.is_valid():
            ser_obj.save()
            res.data = ser_obj.data
        else:
            res.code = 1020
            res.error = ser_obj.errors
        return Response(res.dict)


class LoginView(APIView):
    def post(self, request):
        res = BaseResponse()
        # 下面代码就是说，获取不到用户名，则获取一个空字符串
        username = request.data.get('username', '')
        pwd = request.data.get('pwd', '')
        user_obj = Account.objects.filter(username=username, pwd=pwd).first()
        if not user_obj:
            res.code = 1030
            res.error = '用户名和密码错误'
            return Response(res.dict)
        # 用户登录成功生成一个token写入reids
        # 写入 redis   token: user_id
        conn = redis.Redis(connection_pool=POOL)
        try:
            token = uuid.uuid4()
            # conn.set(str(token), user_obj, ex=123)
            # 我们测试的时候，先将延时取消掉
            conn.set(str(token), user_obj.id)
            res.data = token
        except Exception as e:
            res.code = 1031
            res.error = '创建令牌失败'
        return Response(res.dict)


class TestView(APIView):
    authentication_classes = [LoginAuth, ]

    def get(self, request):
        return Response("认证测试")