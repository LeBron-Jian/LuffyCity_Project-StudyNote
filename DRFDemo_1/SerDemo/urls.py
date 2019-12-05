# _*_coding:utf-8_*_
from django.urls import path, include
# from .views import BookView, BookEditView, BookModelViewSet
from .views import BookModelViewSet

urlpatterns1 = [
    # path('list', BookView.as_view()),
    # path('retrieve/(?P<id>\d+)', BookEditView.as_view()),
    # 在django2.0 之后，改版了，这样命名
    # path('retrieve/<int:id>', BookEditView.as_view()),
    path('list', BookModelViewSet.as_view({"get": "list", "post": "create"})),
    # path('retrieve/(?P<id>\d+)', BookModelViewSet.as_view({'get': 'retrieve',
    #                                                        'put': 'update',
    #                                                        'delete': 'destroy'})),
    path('retrieve/<int:id>', BookModelViewSet.as_view({'get': 'retrieve',
                                                        'put': 'update',
                                                        'delete': 'destroy'})),
]

from rest_framework.routers import DefaultRouter

# 我们注册完成后，它会自动生成一个带参数的路由
router = DefaultRouter()
# 注意：router.register(r"$")如果加$符，会出问题
router.register(r"", BookModelViewSet, basename='books')

urlpatterns = [

]

urlpatterns += router.urls
