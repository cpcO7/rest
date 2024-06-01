from django.urls import path

from apps.views import CourseListAPIView, CourseRetrieveAPIView

urlpatterns = [
    path('course/', CourseListAPIView.as_view()),
    path('course/<int:pk>', CourseRetrieveAPIView.as_view())
]


