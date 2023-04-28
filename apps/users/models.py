import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework_simplejwt.tokens import RefreshToken

from apps.common.models import TimeStampedModel
from apps.users.managers import SoftDeleteUserManager


# Create your models here.
class User(AbstractUser, TimeStampedModel):

    first_name = None
    last_name = None
    username = None
    email = None

    phone_number = PhoneNumberField(region="UZ", unique=True, null=True, verbose_name="Phone number")

    full_name = models.CharField(max_length=40, verbose_name="Full name")
    profile_image = models.ImageField(
        upload_to="profile_images", null=True, blank=True, default="default_user_pic.png", verbose_name="Profile image"
    )
    uuid = models.UUIDField("UUID", unique=True, default=uuid.uuid4, editable=False, db_index=True)

    is_deleted = models.BooleanField("Is deleted", default=False)
    is_active = models.BooleanField("Is active", default=True)
    address = models.CharField("Address", max_length=255, null=True, blank=True)

    objects = SoftDeleteUserManager()
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["full_name", "password"]

    def __str__(self):
        if self.full_name:
            return self.full_name
        if self.phone_number:
            return str(self.phone_number)

    def prepare_to_delete(self):
        self.is_deleted = True
        if self.full_name:
            self.full_name = f"DELETED_{self.id}_{self.full_name}"
        self.phone_number = f"DELETED_{self.id}_{self.phone_number}"
        self.save()

    @property
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
