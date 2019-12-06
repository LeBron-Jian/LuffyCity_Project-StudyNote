from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Food, Coupon
from django.contrib.contenttypes.models import ContentType

# Create your views here.


class DemoView(APIView):
    def get(self, request):
        # 通过ContentType 表找表模型
        content = ContentType.objects.filter(app_label='demo', model='food').first()
        print(content)
        model_class = content.model_class()
        ret = model_class.objects.all()
        print(ret)
        return Response("ContentType测试")
