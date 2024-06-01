from django.db.models import FileField, ForeignKey, CASCADE, ManyToManyField
from django_ckeditor_5.fields import CKEditor5Field

from apps.models import BaseModel
from apps.models.user import User


class Category(BaseModel):
    pass


class Course(BaseModel):
    description = CKEditor5Field()
    video = FileField(upload_to='courses')
    category = ForeignKey('apps.Category', CASCADE, related_name='courses')
    students = ManyToManyField('apps.User', limit_choices_to={"type": User.Type.STUDENT}, related_name='courses',
                               blank=True)
