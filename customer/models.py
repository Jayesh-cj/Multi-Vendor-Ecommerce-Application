from django.db import models
from accounts.models import User

# Create your models here.
class Contacts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_contacts')
    address = models.TextField()