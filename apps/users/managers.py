from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager as djUserManager
from django.db.models import QuerySet


class UserManager(djUserManager):
    def create_user(self, username=None, password=None, **extra_fields):
        return super().create_user(username=username, password=password, **extra_fields)

    def create_superuser(self, username=None, password=None, **extra_fields):
        return super().create_superuser(username=username, password=password, **extra_fields)

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """

        GlobalUserModel = apps.get_model(self.model._meta.app_label, self.model._meta.object_name)
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.password = make_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user


class SoftDeleteUserManager(UserManager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(is_deleted=False)
