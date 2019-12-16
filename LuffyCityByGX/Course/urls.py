# by gaoxin
from django.urls import path
from .views import CategoryView, CourseView, CourseDetailView, CourseChapterView, CourseCommentView, QuestionView
from .video_view import PolyvView


urlpatterns = [
    path('category', CategoryView.as_view()),
    path('list', CourseView.as_view()),
    path('detail/<int:pk>', CourseDetailView.as_view()),
    path('chapter/<int:pk>', CourseChapterView.as_view()),
    path('comment/<int:pk>', CourseCommentView.as_view()),
    path('question/<int:pk>', QuestionView.as_view()),
    path('polyv', PolyvView.as_view()),

]