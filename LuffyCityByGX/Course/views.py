from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from . import models
from .serializers import CategorySerializer, CourseSerializer, CourseDetailSerializer, CourseChapterSerializer
from .serializers import CourseCommentSerializer, QuestionSerializer

# Create your views here.


class CategoryView(APIView):
    def get(self, request):
        # 通过ORM操作获取所有分类数据
        queryset = models.Category.objects.all()
        # 利用序列化器去序列化我们的数据
        ser_obj = CategorySerializer(queryset, many=True)
        # 返回
        return Response(ser_obj.data)


class CourseView(APIView):
    def get(self, request):
        # 获取过滤条件中的分类ID
        category_id = request.query_params.get("category", 0)
        # 根据分类获取课程
        if category_id == 0:
            queryset = models.Course.objects.all().order_by("order")
        else:
            queryset = models.Course.objects.filter(category_id=category_id).all().order_by("order")
        # 序列化课程数据
        ser_obj = CourseSerializer(queryset, many=True)
        # 返回
        return Response(ser_obj.data)


class CourseDetailView(APIView):
    def get(self, request, pk):
        # 根据pk获取到课程详情对象
        course_detail_obj = models.CourseDetail.objects.filter(course__id=pk).first()
        if not course_detail_obj:
            return Response({"code": 1001, "error": "查询的课程详情不存在"})
        # 序列化课程详情
        ser_obj = CourseDetailSerializer(course_detail_obj)
        # 返回
        return Response(ser_obj.data)


class CourseChapterView(APIView):
    def get(self, request, pk):
        # ["第一章": {课时一， 课时二}]
        queryset = models.CourseChapter.objects.filter(course_id=pk).all().order_by("chapter")
        # 序列化章节对象
        ser_obj = CourseChapterSerializer(queryset, many=True)
        # 返回
        return Response(ser_obj.data)


class CourseCommentView(APIView):
    def get(self, request, pk):
        # 通过课程id找到课程所有的评论
        queryset = models.Course.objects.filter(id=pk).first().course_comments.all()
        # 序列化
        ser_obj = CourseCommentSerializer(queryset, many=True)
        # 返回
        return Response(ser_obj.data)


class QuestionView(APIView):
    def get(self, request, pk):
        queryset = models.Course.objects.filter(id=pk).first().often_ask_questions.all()
        ser_obj = QuestionSerializer(queryset, many=True)
        return Response(ser_obj.data)


