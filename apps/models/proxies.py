from apps.models.managers import StudentManager, TeacherManager, AdminManager, ModeratorManager
from apps.models.user import User


class StudentUserProxy(User):
    objects = StudentManager()

    class Meta:
        proxy = True
        verbose_name = "Student"
        verbose_name_plural = "Students"


class TeacherUserProxy(User):
    objects = TeacherManager()

    class Meta:
        proxy = True
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"


class AdminUserProxy(User):
    objects = AdminManager()

    class Meta:
        proxy = True
        verbose_name = "Admin"
        verbose_name_plural = "Admins"


class ModeratorUserProxy(User):
    objects = ModeratorManager()

    class Meta:
        proxy = True
        verbose_name = "Moderator"
        verbose_name_plural = "Moderators"
