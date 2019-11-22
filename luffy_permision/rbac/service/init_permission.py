# _*_coding:utf-8_*_
from django.shortcuts import redirect
from django.conf import settings


def init_permission(current_user, request):
    '''
    用户权限的初始化
    :param current_user: 当前用户对象
    :param request:
    :return:
    '''
    # 2，权限信息初始化
    # 根据当前用户信息获取此用户所拥有的所有权限，并放入session中
    # 如何获取，我们通过表关联
    # 通过.distinct() 进行去重
    # permissions__isnull=False 表示权限不为空，加上这一步
    permission_queryset = current_user.roles.filter(permissions__isnull=False).values(
        'permissions__id',
        'permissions__url',
        'permissions__title',
        'permissions__name',
        'permissions__pid_id',
        'permissions__pid__title',
        'permissions__pid__url',
        'permissions__menu_id',
        'permissions__menu__title',
        'permissions__menu__icon'
    ).distinct()

    # 3，获取权限+菜单信息
    # for item in permission_queryset:
    #     print(item)
    # 上面拿到的permissions__id 是没有用的
    # queryset是不能放在session中
    # 当我们获取当前用户的所有权限后，下面获取权限中的所有URL
    # permission_list = []
    # for item in permission_queryset:
    #     permission_list.append(item['permissions__url'])
    # 上面三行代码可以使用下面列表生成式简化
    # menu_list = []
    # permission_list = []
    # for item in permission_queryset:
    #     permission_list.append(item['permissions__url'])
    #     if item['permissions__is_menu']:
    #         temp = {
    #             'title': item['permissions__title'],
    #             'icon': item['permissions__icon'],
    #             'url': item['permissions__url'],
    #         }
    #         menu_list.append(temp)
    #
    # # permission_list = [item['permissions__url'] for item in permission_queryset]
    # # request.session['luffy_permissions_url_list_key'] = permission_list
    # request.session[settings.PERMISSION_SESSION_KEY] = permission_list
    # request.session[settings.MENU_SESSION_KEY] = menu_list

    # # 获取权限 + 菜单信息
    # menu_dict = {}
    # permission_list = []
    # for item in permission_queryset:
    #     permission_list.append(
    #         {'id': item['permissions__id'],
    #          'url': item['permissions__url'],
    #          'pid': item['permissions__pid_id'],
    #          'p_title':item['permissions__pid__title'],
    #          'p_url': item['permissions__pid__url'],
    #          })
    #
    #     menu_id = item['permissions__menu_id']
    #     # 如果不存在，则不能作为菜单
    #     if not menu_id:
    #         continue
    #
    #     node = {'id': item['permissions__id'],
    #             'title': item['permissions__title'],
    #             'url': item['permissions__url']}
    #
    #     if menu_id in menu_dict:
    #         menu_dict[menu_id]['children'].append(node)
    #     else:
    #         menu_dict[menu_id] = {
    #             'title': item['permissions__menu__title'],
    #             'icon': item['permissions__menu__icon'],
    #             'children': [node, ],
    #         }
    # # print(menu_dict)
    # request.session[settings.PERMISSION_SESSION_KEY] = permission_list
    # request.session[settings.MENU_SESSION_KEY] = menu_dict

    # 获取权限 + 菜单信息
    menu_dict = {}
    # 下面将permission_list 转变成一个字典
    # permission_list = []
    permission_dict = {}
    for item in permission_queryset:
        permission_dict[item['permissions__name']] = {
            'id': item['permissions__id'],
            'title': item['permissions__title'],
            'url': item['permissions__url'],
            'pid': item['permissions__pid_id'],
            'p_title': item['permissions__pid__title'],
            'p_url': item['permissions__pid__url'],
        }

        menu_id = item['permissions__menu_id']
        # 如果不存在，则不能作为菜单
        if not menu_id:
            continue

        node = {'id': item['permissions__id'],
                'title': item['permissions__title'],
                'url': item['permissions__url']}

        if menu_id in menu_dict:
            menu_dict[menu_id]['children'].append(node)
        else:
            menu_dict[menu_id] = {
                'title': item['permissions__menu__title'],
                'icon': item['permissions__menu__icon'],
                'children': [node, ],
            }
    # print(menu_dict)
    request.session[settings.PERMISSION_SESSION_KEY] = permission_dict
    request.session[settings.MENU_SESSION_KEY] = menu_dict
