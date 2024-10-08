from random import randint

from django.contrib.auth.hashers import make_password
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.models import User
from apps.seriaziler import EmailSerializer, EmailConfirmationSerializer, UserModelSerializer, \
    UserCreateModelSerializer
from apps.tasks import send_email


class EmailAPIView(APIView):
    permission_classes = [AllowAny]

    # @swagger_auto_schema(request_body=EmailSerializer)
    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            recipient = serializer.validated_data['recipient']
            try:
                user = User.objects.get(email=recipient)
                return Response({
                    "message": 'Bunday email mavjud boshqa email kiriting! '})
            except ObjectDoesNotExist as e:
                conf_code = randint(10000, 99999)
                cache.set(str(conf_code), recipient, 60)
                send_email.delay([recipient], str(conf_code))
                return Response({"message": "Email sent successfully"})
        return Response(serializer.errors)


class EmailConfirmationAPIView(APIView):
    permission_classes = [AllowAny]

    # @swagger_auto_schema(request_body=EmailConfirmationSerializer)
    def post(self, request):
        serializer = EmailConfirmationSerializer(data=request.data)
        if serializer.is_valid():
            recipient = serializer.validated_data['recipient']
            conf_code = serializer.validated_data['conf_code']
            if cache.get(conf_code) == recipient:
                user, created = User.objects.get_or_create(username=recipient, defaults={'email': recipient})
                refresh = RefreshToken.for_user(user)
                return Response({
                    'message': 'Confirmation successful',
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                })
            else:
                return Response({"error": "Invalid or expired code"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer


class UserCreateAPIView(APIView):
    permission_classes = AllowAny,

    def post(self, request):
        code = request.data.get('code')
        code_data = cache.get(code)
        if code_data:
            User.objects.create_user(**code_data)
            return Response({"message": "User created successfully"}, status.HTTP_201_CREATED)
        return Response({"error": "Invalid or expired code"}, status.HTTP_400_BAD_REQUEST)
