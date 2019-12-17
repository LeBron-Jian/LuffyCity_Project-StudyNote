# _*_coding:utf-8_*_
from django.urls import path
from .views import CategoryView, CourseDetailView, CourseChepterView, CourseCommentView, QuestionView

urlpatterns = [
    path('category', CategoryView.as_view()),
    # path('list?category=0', CategoryView.as_view()),
    path('list', CategoryView.as_view()),
    path('detail/<int:pk>', CourseDetailView.as_view()),
    path('chapter/<int:pk>', CourseChepterView.as_view()),
    path('comment/<int:pk>', CourseCommentView.as_view()),
    path('question/<int:pk>', QuestionView.as_view()),
]
