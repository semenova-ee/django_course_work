from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'null': True, 'blank': True}


# Create your models here.
class User(AbstractUser):

    email = models.EmailField(max_length=150, unique=True, verbose_name='Email')
    phone = models.CharField(max_length=35, verbose_name='номер телефона', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # ROLE_CHOICES = [
    #     ('user', 'User'),
    #     ('moderator', 'Moderator'),
    # ]

    # role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    #
    #
    # def has_moderator_permissions(self):
    #     return self.role == 'moderator'

    # class Meta:
    #     permissions = [
    #         ("can_cancel_post", "Can cancel blog post"),
    #         ("can_change_product_description", "Can change product description"),
    #         ("can_change_product_category", "Can change product category"),
    #     ]

    def __str__(self):
        return self.email
