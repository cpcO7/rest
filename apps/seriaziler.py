from rest_framework.serializers import ModelSerializer, EmailField, Serializer, CharField

from apps.models import Course, User


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = 'id', 'username', 'type'


class CourseModelSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

    def to_representation(self, instance: Course):
        represent = super().to_representation(instance)
        represent['teacher'] = UserModelSerializer(instance.teacher).data
        return represent


class EmailSerializer(Serializer):
    recipient = EmailField()


class EmailConfirmationSerializer(Serializer):
    recipient = EmailField()
    conf_code = CharField(max_length=5)


class UserCreateModelSerializer(ModelSerializer):
    code = CharField(max_length=5, write_only=True)

    class Meta:
        model = User
        fields = 'code',




