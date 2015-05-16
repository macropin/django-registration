# coding: utf-8

try:
    from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
except ImportError:
    from django.contrib.auth.models import User as AbstractBaseUser, UserManager as BaseUserManager

from django.db import models


class CustomUser(AbstractBaseUser):
    new_field = models.CharField(max_length=25)
    objects = BaseUserManager()

    USERNAME_FIELD = 'new_field'
