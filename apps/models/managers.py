from django.contrib.auth.models import UserManager


class AdminManager(UserManager):

    def get_queryset(self):
        return super().get_queryset().filter(type=self.model.Type.ADMIN)


class StudentManager(UserManager):

    def get_queryset(self):
        return super().get_queryset().filter(type=self.model.Type.STUDENT)


class TeacherManager(UserManager):

    def get_queryset(self):
        return super().get_queryset().filter(type=self.model.Type.TEACHER)


class ModeratorManager(UserManager):

    def get_queryset(self):
        return super().get_queryset().filter(type=self.model.Type.MODERATOR)
