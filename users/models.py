from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    active = models.BooleanField(_('active'), default=True)

    is_staff = models.BooleanField(_('is_staff'), default=False)
    is_superuser = models.BooleanField(_('is_superuser'), default=False)

    created_on = models.DateTimeField(_('created on'), auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(_('updated on'), auto_now=True)

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "User"
