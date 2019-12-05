#_*_coding:utf-8_*_
from django.urls import path, include
from .views import DemoView

urlpatterns = [
    path(r"", DemoView.as_view())
]