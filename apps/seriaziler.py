from rest_framework.serializers import ModelSerializer

from apps.models import Course


class CourseModelSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = 'id', 'title'
