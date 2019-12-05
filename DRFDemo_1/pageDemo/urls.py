#_*_coding:utf-8_*_
from django.urls import path
from .views import BookView

urlpatterns = [
    path('book', BookView.as_view())
]