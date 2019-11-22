# _*_coding:utf-8_*_
from django.shortcuts import render, redirect, reverse, HttpResponse
from rbac import models
from rbac.forms.menu import MenuModelForm, SecondMenuModelForm, PermissionModelForm
from rbac.service.urls import memory_reverse


def menu_list(request):
    '''
    菜单和权限列表
    :param request:
    :return:
    '''
    menus = models.Menu.objects.all()
    # 我们在后台需要接受一下mid的值
    # print(menus)
    menu_id = request.GET.get('mid')  # 用户选择的一级菜单
    second_menu_id = request.GET.get('sid')  # 用户选择的2级菜单

    menus_exists = models.Menu.objects.filter(id=menu_id).filter(id=menu_id).exists()
    if not menus_exists:
        menu_id = None
    if menu_id:
        second_menus = models.Permission.objects.filter(menu_id=menu_id)
    else:
        second_menus = []

    second_menu_exists = models.Permission.objects.filter(id=second_menu_id).exists()
    if not second_menu_exists:
        second_menu_id = None

    if second_menu_id:
        permissions = models.Permission.objects.filter(pid_id=second_menu_id)
    else:
        permissions = []

    return render(
        request, 'rbac/menu_list.html',
        {
            'menus': menus,
            'second_menus': second_menus,
            'permissions': permissions,
            'menu_id': menu_id,
            'second_menu_id': second_menu_id,

        }
    )


def menu_add(request):
    '''
    添加一级菜单
    :param request:
    :return:
    '''
    if request.method == 'GET':
        form = MenuModelForm()
        return render(request, 'rbac/change.html', {'form': form})

    form = MenuModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'rbac:menu_list'))
    return render(request, 'rbac/change.html', {'form': form})


def menu_edit(request, pk):
    '''
    编辑功能
    :param request:
    :param pk:
    :return:
    '''
    obj = models.Menu.objects.filter(id=pk).first()
    if not obj:
        return HttpResponse("菜单不存在")
    if request.method == 'GET':
        form = MenuModelForm(instance=obj)
        return render(request, 'rbac/change.html', {'form': form})
    form = MenuModelForm(instance=obj, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'rbac:menu_list'))
    return render(request, 'rbac/change.html', {'form': form})


def menu_del(request, pk):
    '''
    删除功能
    :param request:
    :param pk:
    :return:
    '''
    url = memory_reverse(request, 'rbac:menu_list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': url})
    models.Menu.objects.filter(id=pk).delete()
    return redirect(url)


def second_menu_add(request, menu_id):
    '''
    添加二级菜单
    :param request:
    :param menu_id:已选择的一级菜单ID（用于设置默认值）
    :return:
    '''
    menu_object = models.Menu.objects.filter(id=menu_id).first()

    if request.method == 'GET':
        form = SecondMenuModelForm(initial={'menu': menu_object})
        return render(request, 'rbac/change.html', {'form': form})

    form = SecondMenuModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'rbac:menu_list'))
    return render(request, 'rbac/change.html', {'form': form})


def second_menu_edit(request, pk):
    '''
    编辑二级菜单
    :param request:
    :param menu_id:已选择的一级菜单ID（用于设置默认值）
    :return:
    '''
    permission_object = models.Permission.objects.filter(id=pk).first()

    if request.method == 'GET':
        form = SecondMenuModelForm(instance=permission_object)
        return render(request, 'rbac/change.html', {'form': form})

    form = SecondMenuModelForm(data=request.POST, instance=permission_object)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'rbac:menu_list'))
    return render(request, 'rbac/change.html', {'form': form})


def second_menu_del(request, pk):
    '''
    删除功能
    :param request:
    :param pk:
    :return:
    '''
    url = memory_reverse(request, 'rbac:menu_list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': url})
    models.Permission.objects.filter(id=pk).delete()
    return redirect(url)

def permission_add(request, second_menu_id):
    '''
    添加权限
    :param request:
    :param second_menu_id:
    :return:
    '''
    if request.method == 'GET':
        form = PermissionModelForm()
        return render(request, 'rbac/change.html', {'form': form})

    form = PermissionModelForm(data=request.POST)
    if form.is_valid():
        # 先做一次查询
        second_menu_object = models.Permission.objects.filter(id=second_menu_id).first()
        if not second_menu_object:
            return HttpResponse("二级菜单不存在， 请重新选择！")
        # form.intance 中包含用户提交的所有值
        # instance = models.Permission(title='', name='', url='', pid=second_menu_object)
        form.instance.pid = second_menu_object
        # form.instance = second_menu_object
        form.save()  # 这一步是保存到数据库中
        return redirect(memory_reverse(request, 'rbac:menu_list'))
    return render(request, 'rbac/change.html', {'form': form})


def permission_edit(request, pk):
    '''
    编辑权限
    :param request:
    :param menu_id:已选择的一级菜单ID（用于设置默认值）
    :return:
    '''
    permission_object = models.Permission.objects.filter(id=pk).first()

    if request.method == 'GET':
        form = PermissionModelForm(instance=permission_object)
        return render(request, 'rbac/change.html', {'form': form})

    form = PermissionModelForm(data=request.POST, instance=permission_object)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'rbac:menu_list'))
    return render(request, 'rbac/change.html', {'form': form})


def permission_del(request, pk):
    '''
    删除权限
    :param request:
    :param pk:
    :return:
    '''
    url = memory_reverse(request, 'rbac:menu_list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': url})
    models.Permission.objects.filter(id=pk).delete()
    return redirect(url)
