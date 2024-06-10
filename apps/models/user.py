import uuid

from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.functions import RandomUUID
from django.db.models import ImageField, TextChoices, CharField, UUIDField


class User(AbstractUser):
    class Type(TextChoices):
        ADMIN = 'admin', 'Admin'
        MODERATOR = 'moderator', 'Moderator'
        TEACHER = 'teacher', 'Teacher'
        STUDENT = 'student', 'Student'

    id = UUIDField(primary_key=True, db_default=RandomUUID(), editable=False)
    image = ImageField(upload_to='users/', blank=True, null=True)
    phone_number = CharField(max_length=20, blank=True, null=True)
    type = CharField(max_length=20, choices=Type.choices, db_default=Type.STUDENT)
