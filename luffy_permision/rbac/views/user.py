# _*_coding:utf-8_*_

'''
用户管理
'''
from django.shortcuts import render, redirect, HttpResponse
from rbac import models
from django import forms
from django.urls import reverse

from rbac.forms.user import UserModelForm, UpdateUserModelForm, ResetPasswordUserModelForm


def user_list(request):
    '''
    用户列表
    :param request:
    :return:
    '''
    user_queryset = models.UserInfo.objects.all()
    print(user_queryset)
    return render(request, 'rbac/user_list.html', {'users': user_queryset})


def user_add(request):
    '''
    添加角色
    :param request:
    :return:
    '''
    if request.method == 'GET':
        form = UserModelForm()
        return render(request, 'rbac/change.html', {'form': form})

    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:user_list'))
    return render(request, 'rbac/change.html', {'form': form})


def user_edit(request, pk):
    '''
    编辑用户
    :param request:
    pk：要修改的用户ID
    :return:
    '''
    obj = models.UserInfo.objects.filter(id=pk).first()
    if not obj:
        # 当然这里404可以写一个页面，这里为了简单起见，所以直接返回
        return HttpResponse("角色不存在")
    if request.method == 'GET':
        form = UpdateUserModelForm(instance=obj)
        return render(request, 'rbac/change.html', {'form': form})

    form = UpdateUserModelForm(instance=obj, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:user_list'))
    return render(request, 'rbac/change.html', {'form': form})


def user_reset_pwd(request, pk):
    '''
    重置密码
    :param request:
    :return:
    '''
    obj = models.UserInfo.objects.filter(id=pk).first()
    if not obj:
        return HttpResponse("用户不存在")
    if request.method == 'GET':
        form = ResetPasswordUserModelForm()
        return render(request, 'rbac/change.html', {'form': form})

    form = ResetPasswordUserModelForm(instance=obj, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:user_list'))
    return render(request, 'rbac/change.html', {'form': form})

def user_del(request, pk):
    '''
    删除角色
    下面我们希望不是一下删除，为了防止误操作，我们添加一个页面，让用户确认再删除。
    :param request:
    :param pk: 要删除的角色ID
    :return:
    '''
    origin_url = reverse('rbac:user_list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': origin_url})
    models.UserInfo.objects.filter(id=pk).delete()
    return redirect(origin_url)
