from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

class CustomerUser(AbstractUser):
    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="customeruser_set",
        related_query_name="customeruser",
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="customeruser_set",
        related_query_name="customeruser",
    )



