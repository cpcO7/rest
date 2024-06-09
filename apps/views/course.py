from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView

from apps.models import Course
from apps.seriaziler import CourseModelSerializer


class CourseListAPIView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseModelSerializer


class CourseRetrieveAPIView(RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseModelSerializer
