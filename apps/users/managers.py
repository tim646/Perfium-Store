from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import BaseUserManager
from django.db.models import QuerySet


class UserManager(BaseUserManager):
    def create_user(self, full_name=None, password=None, **extra_fields):
        return super().create_user(full_name=full_name, password=password, **extra_fields)

    def create_superuser(self, full_name=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(full_name=full_name, password=password, **extra_fields)

    def _create_user(self, full_name, password, **extra_fields):
        """
        Create and save a user with the given full name and password.
        """

        GlobalUserModel = apps.get_model(self.model._meta.app_label, self.model._meta.object_name)
        full_name = GlobalUserModel.normalize_username(full_name)
        user = self.model(full_name=full_name, **extra_fields)
        user.password = make_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user


class SoftDeleteUserManager(UserManager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(is_deleted=False)
