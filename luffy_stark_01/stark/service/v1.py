# _*_coding:utf-8_*_
from django.shortcuts import HttpResponse, render
from django.conf.urls import url


class StarkHandler(object):
    def __init__(self, model_class, prev):
        self.model_class = model_class
        self.prev = prev

    def changelist_view(self, request):
        '''
        列表页面
        :param request:
        :return:
        '''
        # 访问http://127.0.0.1:8000/stark/app01/depart/list/； self.model_class = app01.models.Depart
        # 访问http://127.0.0.1:8000/stark/app01/userinfo/list/； self.model_class = app01.models.UserInfo
        # 访问http://127.0.0.1:8000/stark/app02/role/list/； self.model_class = app02.models.Role
        # 访问http://127.0.0.1:8000/stark/app02/host/list/； self.model_class =app02.models.Host
        # self.models_class
        # print(self.model_class)
        data_list = self.model_class.objects.all()
        # print(data_list)
        return render(request, 'stark/changelist.html', {'data_list': data_list})

    def add_view(self, request):
        '''
        添加页面
        :param request:
        :return:
        '''
        # self.models_class
        return HttpResponse("添加页面")

    def change_view(self, request):
        '''
        修改页面
        :param request:
        :return:
        '''
        # self.models_class
        return HttpResponse("修改页面")

    def delete_view(self, request):
        '''
        删除页面
        :param request:
        :return:
        '''
        # self.models_class
        return HttpResponse("删除页面")

    def get_url_name(self, param):
        app_label, model_name = self.model_class._meta.app_label, self.model_class._meta.model_name
        if self.prev:
            return "%s_%s_%s_%s"%(app_label, model_name, self.prev, param)
        return '%s_%s_%s'%(app_label, model_name, param)

    @property
    def get_list_url_name(self):
        '''
        获取列表页面URL的name
        :return:
        '''
        return self.get_url_name('list')

    @property
    def get_add_url_name(self):
        '''
        添加页面URL的name
        :return:
        '''
        return self.get_url_name('add')

    @property
    def get_change_url_name(self):
        '''
        获取修改页面URL的name
        :return:
        '''
        return self.get_url_name('change')

    @property
    def get_delete_url_name(self):
        '''
        获取删除页面URL的name
        :return:
        '''
        return self.get_url_name('delete')

    def get_urls(self):
        patterns = [
            url(r'^list/$', self.changelist_view, name=self.get_list_url_name),
            url(r'^add/$', self.add_view, name=self.get_add_url_name),
            url(r'^change/(\d+)/$', self.change_view, name=self.get_change_url_name),
            url(r'^delete/(\d+)/$', self.delete_view, name=self.get_delete_url_name),
        ]

        patterns.extend(self.extra_urls())
        return patterns

    def extra_urls(self):
        return []


class StarkSite(object):
    def __init__(self):
        self._registry = []
        self.app_name = 'stark'
        self.namespace = 'stark'

    def register(self, model_class, handler_class=None, prev=None):
        '''

        :param model_class: 是models中的数据库相关类
        :param prev  URL的前缀
        :return:
        '''
        if not handler_class:
            handler_class = StarkHandler
        self._registry.append({'model_class': model_class, 'handler': handler_class(model_class, prev), 'prev': prev})

    def get_urls(self):
        patterns = []
        for item in self._registry:
            model_class = item['model_class']
            handler = item['handler']
            prev = item['prev']
            app_label, model_name = model_class._meta.app_label, model_class._meta.model_name

            if prev:
                # patterns.append(url(r'%s/%s/%s/list/$' % (app_label, model_name, prev,), handler.changelist_view))
                # patterns.append(url(r'%s/%s/%s/add/$' % (app_label, model_name, prev,), handler.add_view))
                # patterns.append(url(r'%s/%s/%s/change/(\d+)/$' % (app_label, model_name, prev,), handler.change_view))
                # patterns.append(url(r'%s/%s/%s/list/(\d+)/$' % (app_label, model_name, prev,), handler.change_view))
                patterns.append(url(r'%s/%s/%s/' % (app_label, model_name, prev,), (handler.get_urls(), None, None)))
            else:
                # patterns.append(url(r'%s/%s/list/$' % (app_label, model_name,), handler.changelist_view))
                # patterns.append(url(r'%s/%s/add/$' % (app_label, model_name,), handler.add_view))
                # patterns.append(url(r'%s/%s/change/(\d+)/$' % (app_label, model_name,), handler.change_view))
                # patterns.append(url(r'%s/%s/list/(\d+)/$' % (app_label, model_name,), handler.change_view))
                patterns.append(url(r'%s/%s/' % (app_label, model_name,), (handler.get_urls(), None, None)))

            # patterns.append(url(r'x1/', lambda request: HttpResponse('x1')), )
            # patterns.append(url(r'x2/', lambda request: HttpResponse('x2')), )
        return patterns

    @property
    def urls(self):
        return self.get_urls(), self.app_name, self.namespace


site = StarkSite()
