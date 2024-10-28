import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.manager import UserManager

from base.email import send_account_activation_email

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE = (
        ('Customer', 'Customer'),
        ('Vendor', 'Vendor')
    )

    uid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True) 
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    profile = models.FileField(upload_to='profile/', default='profile/default_profile.jpg')
    email_token = models.CharField(max_length=100, null=True, blank=True)
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
    
@receiver(post_save, sender = User)
def send_email_token(sender, instance, created, **kwargs):
    try:
        if created:
            token = str(uuid.uuid4)
            user = User.objects.get(uid = instance.uid)
            user.email_token = token
            user.save()
            email = user.email
            send_account_activation_email(email, token)
    except Exception as e:
        print(e)