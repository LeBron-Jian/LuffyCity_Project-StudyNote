#_*_coding:utf-8_*_
from rest_framework.permissions import BasePermission

class MyPermission(BasePermission):
    message = '您没有权限'
    def has_permission(self, request, view):
        # 判断用户是否有权限
        user_obj = request.user
        if user_obj.type == 3:
            return False
        else:
            return True