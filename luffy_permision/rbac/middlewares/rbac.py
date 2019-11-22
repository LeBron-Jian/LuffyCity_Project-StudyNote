# _*_coding:utf-8_*_
import re
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse
from django.conf import settings


class RbacMiddleware(MiddlewareMixin):
    '''
    用户权限信息校验
    '''

    def process_request(self, request):
        '''
        当用户请求刚进入的时候出发执行
        1， 获取当前用户请求的url
        2，获取当前用户在session中保存的权限列表['/customer/list/','/customer/add/'....]
        3，权限信息匹配
        :param request:
        :return:
        '''
        # 使用正则匹配，那么就包括了很多匹配，比==能包含的情况多

        # 如果访问的是http://127.0.0.1:8000/customer/list/——》path_info就是/customer/list/
        current_url = request.path_info
        for valid_url in settings.VALID_URL_LIST:
            if re.match(valid_url, current_url):
                # if valid_url == current_url:
                #     pass  # 白名单中的URL无需权限验证即可访问
                return None

        # permission_list = request.session.get['luffy_permissions_url_list_key']
        permission_dict = request.session.get(settings.PERMISSION_SESSION_KEY)
        print(permission_dict)
        if not permission_dict:
            return HttpResponse("未获取到用户信息，请重新登录")

        flag = False
        # print(current_url)
        url_record = [
            {'title': '首页', 'url': '#'}
        ]
        for item in permission_dict.values():
            # 下面匹配的时候使用正则表达式进行匹配
            # 拥有权限可以访问
            # 正则匹配，匹配成功则返回，不成功则返回None
            # 正则匹配，保证起始和终止符^ $
            reg = "^%s$" % item['url']
            if re.match(reg, current_url):
                # pass  # 拥有权限可以访问
                flag = True
                request.current_selected_permission = item['pid'] or item['id']
                if not item['pid']:
                    url_record.extend([
                        {'title': item['title'], 'url': item['url'], 'class':'active'}
                    ])
                else:
                    url_record.extend([
                        {'title': item['p_title'], 'url': item['p_url']},
                        {'title': item['title'], 'url': item['url'], 'class':'active'},
                    ])
                request.breadcrumb = url_record
                break
        # flag等于False表示无权访问
        if not flag:
            return HttpResponse("无权访问")
