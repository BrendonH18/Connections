from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

class CustomUser(AbstractUser, PermissionsMixin):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(max_length=255, null=False, blank=False)
    last_name = models.CharField(max_length=255, null=False, blank=False)
    avatar = models.CharField(max_length=255, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = ["first_name", "last_name"]

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.get_full_name()