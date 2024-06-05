from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.views import CourseListAPIView, CourseRetrieveAPIView, EmailAPIView, EmailConfirmationAPIView, UserListAPIView

urlpatterns = [
    path('course/', CourseListAPIView.as_view()),
    path('course/<int:pk>', CourseRetrieveAPIView.as_view()),
    path('user/', UserListAPIView.as_view()),

    path('send-email/', EmailAPIView.as_view()),
    path('conf-email/', EmailConfirmationAPIView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view())
]
