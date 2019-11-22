# _*_coding:utf-8_*_

from django.shortcuts import HttpResponse, render, redirect
# 用户表在rbac中，我们暂时使用rbac的用户表
# TODO  我们需要建立web（业务中）的用户表
from rbac import models
from rbac.service.init_permission import init_permission


def login(request):
    # 1，用户登录
    if request.method == 'GET':
        return render(request, 'login.html')
    # 获取到登录页面的信息，下面获取账号和密码
    # 按理说，我们这里需要加上form组件等
    user = request.POST.get('user')
    pwd = request.POST.get('pwd')

    current_user = models.UserInfo.objects.filter(name=user, password=pwd).first()
    if not current_user:
        return render(request, 'login.html', {'msg': '用户名或密码错误'})

    init_permission(current_user, request)

    # 当登录成功后，我们需要将页面重定向到首页。

    return redirect('/customer/list/')
