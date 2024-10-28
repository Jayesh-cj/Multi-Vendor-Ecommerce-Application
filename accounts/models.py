from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.manager import UserManager

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE = (
        ('Customer', 'Customer'),
        ('Vendor', 'Vendor')
    )

    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    profile = models.FileField(upload_to='profile/')
    email_token = models.IntegerField()
    is_verified = models.BooleanField(default=False)
    user_type = models.CharField(max_length=50, choices=USER_TYPE)
    password = models.CharField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self) -> str:
        return self.username