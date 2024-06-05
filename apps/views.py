from random import randint
from time import time

from drf_yasg.utils import swagger_auto_schema
from redis_dict import RedisDict
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.models import Course, User
from apps.seriaziler import CourseModelSerializer, EmailSerializer, EmailConfirmationSerializer, UserModelSerializer
from apps.tasks import send_email

data = RedisDict(namespace='confirmation')


class CourseListAPIView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseModelSerializer


class CourseRetrieveAPIView(RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseModelSerializer


class EmailAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=EmailSerializer)
    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            recipient = serializer.validated_data['recipient']
            conf_code = randint(10000, 99999)
            data[recipient] = {"code": str(conf_code), "time": time()}
            send_email.delay([recipient], str(conf_code))
            return Response({"message": "Email sent successfully"})
        return Response(serializer.errors)


class EmailConfirmationAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=EmailConfirmationSerializer)
    def post(self, request):
        serializer = EmailConfirmationSerializer(data=request.data)
        if serializer.is_valid():
            recipient = serializer.validated_data['recipient']
            conf_code = serializer.validated_data['conf_code']
            if data.get(recipient) and (time() - data.get(recipient)['time']) < 60 and \
                    data.pop(recipient)['code'] == conf_code:
                user, created = User.objects.get_or_create(username=recipient, defaults={'email': recipient})
                refresh = RefreshToken.for_user(user)
                return Response({
                    'message': 'Confirmation successful',
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                })
            else:
                return Response({'message': 'Code is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
