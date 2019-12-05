# _*_coding:utf-8_*_
from django.urls import path
from .views import DjangoView, DRFView

urlpatterns = [
    path('demo', DjangoView.as_view()),
    path('test', DRFView.as_view())
]
