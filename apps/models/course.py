import uuid

from django.db.models import FileField, ForeignKey, CASCADE, ManyToManyField, UUIDField
from django_ckeditor_5.fields import CKEditor5Field

from apps.models import BaseModel
from apps.models.user import User


class Category(BaseModel):
    id = UUIDField(default=uuid.uuid4, primary_key=True)


class Course(BaseModel):
    id = UUIDField(default=uuid.uuid4, primary_key=True)
    description = CKEditor5Field()
    video = FileField(upload_to='courses')
    category = ForeignKey('apps.Category', CASCADE, related_name='courses')
    teacher = ForeignKey('apps.User', CASCADE, limit_choices_to={"type": User.Type.TEACHER}, related_name='teacher')
    students = ManyToManyField('apps.User', limit_choices_to={"type": User.Type.STUDENT}, related_name='courses',
                               blank=True)
