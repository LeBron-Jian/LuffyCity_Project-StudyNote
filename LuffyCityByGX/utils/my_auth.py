# by gaoxin
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .redis_pool import POOL
from Course.models import Account
import redis



CONN = redis.Redis(connection_pool=POOL)


class LoginAuth(BaseAuthentication):
    def authenticate(self, request):
        # 从请求头中获取前端带过来的token
        token = request.META.get("HTTP_AUTHENTICATION", "")
        if not token:
            raise AuthenticationFailed("没有携带token")
        # 去redis比对
        user_id = CONN.get(str(token))
        if user_id == None:
            raise AuthenticationFailed("token过期")
        user_obj = Account.objects.filter(id=user_id).first()
        return user_obj, token