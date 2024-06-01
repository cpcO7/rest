from django.contrib.auth.models import AbstractUser
from django.db.models import ImageField, TextChoices, CharField


class User(AbstractUser):
    class Type(TextChoices):
        ADMIN = 'admin', 'Admin'
        MODERATOR = 'moderator', 'Moderator'
        TEACHER = 'teacher', 'Teacher'
        STUDENT = 'student', 'Student'

    image = ImageField(upload_to='users/', blank=True, null=True)
    type = CharField(max_length=20, choices=Type.choices, db_default=Type.STUDENT)
