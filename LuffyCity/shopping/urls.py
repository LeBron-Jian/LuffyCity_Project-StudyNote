# _*_coding:utf-8_*_
from django.urls import path
from .views import ShoppingCarView
from .settlement_views import SettlementView

urlpatterns = [
    path('shopping_car', ShoppingCarView.as_view()),
    path('settlement', SettlementView.as_view()),
]
