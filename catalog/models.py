from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

class CustomerUser(AbstractUser):
    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
