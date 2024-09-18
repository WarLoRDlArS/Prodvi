from django.db import models

# Create your models here.

from users.models import Users

class Employee(models.Model):
    user = models.ForeignKey(to=Users, on_delete=models.CASCADE, default=None)

class Manager(models.Model):
    user = models.ForeignKey(to=Users, on_delete=models.CASCADE, default=None)
