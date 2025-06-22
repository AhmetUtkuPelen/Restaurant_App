from django.db import models
from django.contrib.auth.models import AbstractUser
from enum import Enum

# Create your models here.


class UserRole(Enum):
    ADMIN = 'admin'
    USER = 'user'


class UserModel(AbstractUser):
    name = models.CharField(max_length=255,null=False,blank=False)
    email = models.EmailField(max_length=255,unique=True,null=False,blank=False)
    password = models.CharField(max_length=255,null=False,blank=False)
    role = models.CharField(max_length=50, choices=[(tag.name, tag.value) for tag in UserRole], default=UserRole.USER)


    def __str__(self):
        return self.name