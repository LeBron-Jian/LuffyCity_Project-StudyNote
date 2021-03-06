# _*_coding:utf-8_*_
from django.urls import path
from .views import RegisterView, LoginView, TestView

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('test', TestView.as_view()),
]
