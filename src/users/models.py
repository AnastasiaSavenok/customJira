from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from . import managers


class UserType(models.TextChoices):
    EMPLOYEE = 'employee'
    CUSTOMER = 'customer'


class CustomUser(AbstractUser):
    username = None
    name = models.CharField(_("Name of User"), max_length=255)
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(_('phone number'), max_length=13, unique=True)
    user_type = models.CharField(max_length=20, choices=UserType.choices, default=UserType.EMPLOYEE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = managers.CustomUserManager()

    def __str__(self):
        return self.email
