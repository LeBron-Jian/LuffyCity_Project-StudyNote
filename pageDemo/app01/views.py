from django.shortcuts import render
from .models import Book
from django.core.paginator import Paginator, EmptyPage


# Create your views here.
def index(request):
    # insert data to sqlite  not recommend
    # for i in range(100):
    #     Book.objects.create(title="book_%s" % i, price=i * i)

    # insert data to sqlite  recommend
    # finish to append data annotation the code
    # book_list = []
    # for i in range(100):
    #     book = Book(title="book_%s" % i, price=i * 2)
    #     print(book)
    #     book_list.append(book)
    #
    # Book.objects.bulk_create(book_list)

    book_list = Book.objects.all()
    # paginator 分页器需要两个参数,一个object_list  一个 per_page
    paginator = Paginator(book_list, 10)
    # 数据总数
    print("count", paginator.count)
    # 总页数
    print('num_pages', paginator.num_pages)
    # 页码的列表范围
    print('page_range', paginator.page_range)

    # 去前端拿到对应的页数
    current_page_num = int(request.GET.get('page', 1))

    if paginator.num_pages > 1:
        if current_page_num - 5 < 1:
            # 这里写的（1， 11） 是我们要显示10个按钮
            page_range = range(1, 12)
        elif current_page_num + 5 > paginator.num_pages:
            page_range = range(paginator.num_pages - 10, paginator.num_pages + 1)
        else:
            # range 也是顾头不够尾
            page_range = range(current_page_num - 5, current_page_num + 6)
    else:
        page_range = paginator.page_range

    try:
        current_page = paginator.page(current_page_num)

        # 显示某一页具体数据的两种方式
        print("object_list", current_page.object_list)
        for i in current_page:
            print(i)
    except EmptyPage as e:
        # 如果出现的是负数，或者大于页码的数，我们默认让其显示第一页
        current_page = paginator.page(1)

    return render(request, 'index.html', locals())
