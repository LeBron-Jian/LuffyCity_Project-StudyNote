#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
角色管理
"""
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse

from rbac import models
from rbac.forms.role import RoleModelForm


def role_list(request):
    """
    角色列表
    :param request:
    :return:
    """
    role_queryset = models.Role.objects.all()

    return render(request, 'rbac/role_list.html', {'roles': role_queryset})


def role_add(request):
    """
    添加角色
    :param request:
    :return:
    """
    if request.method == 'GET':
        form = RoleModelForm()
        return render(request, 'rbac/change.html', {'form': form})

    form = RoleModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:role_list'))

    return render(request, 'rbac/change.html', {'form': form})


def role_edit(request, pk):
    """
    编辑角色
    :param request:
    :param pk: 要修改的角色ID
    :return:
    """
    obj = models.Role.objects.filter(id=pk).first()
    if not obj:
        # 当然这里404可以写一个页面，这里为了简单起见，所以直接返回
        return HttpResponse('角色不存在')
    if request.method == 'GET':
        form = RoleModelForm(instance=obj)
        return render(request, 'rbac/change.html', {'form': form})

    form = RoleModelForm(instance=obj, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:role_list'))

    return render(request, 'rbac/change.html', {'form': form})


def role_del(request, pk):
    """
    删除角色
    下面我们希望不是一下删除，为了防止误操作，我们添加一个页面，让用户确认再删除。
    :param request:
    :param pk:
    :return:
    """
    origin_url = reverse('rbac:role_list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': origin_url})

    models.Role.objects.filter(id=pk).delete()
    return redirect(origin_url)
