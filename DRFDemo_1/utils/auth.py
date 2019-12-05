# _*_coding:utf-8_*_
from rest_framework.exceptions import AuthenticationFailed
from authDemo.models import User
from rest_framework.authentication import BaseAuthentication

class MyAuth(BaseAuthentication):

    def authenticate(self, request):
        # 做认证，看他是否登录
        # 从url过滤条件里拿到token
        # 去数据库看token是否合法
        # 合法的token能够获取用户信息
        token = request.query_params.get("token", "")
        if not token:
            raise AuthenticationFailed("没有携带token")
        user_obj = User.objects.filter(token=token).first()
        if not user_obj:
            raise AuthenticationFailed("Token不合法")
        # return (None, None)
        return (user_obj, token)