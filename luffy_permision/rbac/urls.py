#_*_coding:utf-8_*_
from django.contrib import admin
from django.urls import re_path, include, path
from django.conf.urls import url
from rbac.views import role
from rbac.views import user
from rbac.views import menu

urlpatterns = [
    re_path(r'^role/list/$', role.role_list, name='role_list'),  # rbac:role_list
    re_path(r'^role/add/$', role.role_add, name='role_add'),  # rbac:role_add
    re_path(r'^role/edit/(?P<pk>\d+)/$', role.role_edit, name='role_edit'),  # rbac:role_edit
    re_path(r'^role/del/(?P<pk>\d+)/$', role.role_del, name='role_del'),  # rbac:role_del

    re_path(r'^user/list/$', user.user_list, name='user_list'),
    re_path(r'^user/add/$', user.user_add, name='user_add'),
    re_path(r'^user/edit/(?P<pk>\d+)/$', user.user_edit, name='user_edit'),
    re_path(r'^user/del/(?P<pk>\d+)/$', user.user_del, name='user_del'),
    re_path(r'^user/reset/password/(?P<pk>\d+)/$', user.user_reset_pwd, name='user_reset_pwd'),

    re_path(r'^menu/list/$', menu.menu_list, name='menu_list'),
    re_path(r'^menu/add/$', menu.menu_add, name='menu_add'),
    re_path(r'^menu/edit/(?P<pk>\d+)/$', menu.menu_edit, name='menu_edit'),
    re_path(r'^menu/del/(?P<pk>\d+)/$', menu.menu_del, name='menu_del'),

    # 二级菜单没有菜单页面
    re_path(r'^second/add/(?P<menu_id>\d+)/$', menu.second_menu_add, name='second_menu_add'),
    re_path(r'^second/edit/(?P<pk>\d+)/$', menu.second_menu_edit, name='second_menu_edit'),
    re_path(r'^second/del/(?P<pk>\d+)/$', menu.second_menu_del, name='second_menu_del'),

    re_path(r'^permission/add/(?P<second_menu_id>\d+)/$', menu.permission_add, name='permission_add'),
    re_path(r'^permission/edit/(?P<pk>\d+)/$', menu.permission_edit, name='permission_edit'),
    re_path(r'^permission/del/(?P<pk>\d+)/$', menu.permission_del, name='permission_del'),

]
