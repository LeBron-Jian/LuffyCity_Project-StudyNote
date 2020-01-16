###分页组件的应用的示例方法

##### 1，后端调用方法
- 可以自己设置 per_page_count，组件中的 per_page_count设置为20，我们自己可以让每页获取的数据设置为10,15,20等等。
- 获取表数据中的数据总数（all_count = self.model_class.objects.all().count()） 
- 获取 query_params 这是一个QueryDict对象，内部含所有当前URL的原条件——我们使用 request_parmas = request.GET.copy()  复制一份URL地址，然后调用
- 调用方法如下：
>
        # ########## 1. 处理分页 ##########
        all_count = self.model_class.objects.all().count()
        query_params = request.GET.copy()
        query_params._mutable = True

        pager = Pagination(
            current_page=request.GET.get('page'),
            all_count=all_count,
            base_url=request.path_info,
            query_params=query_params,
            per_page=self.per_page_count,
        )
        
        data_list = self.model_class.objects.all()[pager.start:pager.end]
- 同时我们要将pager传给前端
>
        return render(
            request,
            'testchange.html',
            {
                'pager':pager
            }
        )
##### 2，前端调用方法
- 在前端调用的方法如下：
>
        <nav>
            <ul class="pagination">
                {{ pager.page_html|safe }}
            </ul>
        </nav>
