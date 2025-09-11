from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField(blank=False, null=False)
    token = models.CharField(blank=True, unique=True)
    password = models.CharField(blank=True, null=True, unique=True)
    profilepic = models.ImageField()
    is_deleted = models.BooleanField(default=False, blank=False, null=False)
