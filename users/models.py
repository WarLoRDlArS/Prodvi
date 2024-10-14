from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, pid, password=None, **extra_fields):
        if not pid:
            raise ValueError('The PID field must be set')
        user = self.model(pid=pid, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, pid=None, password=None, **extra_fields): 
        if not pid:
            raise ValueError('The PID field must be set for superuser')
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # Set the username
        extra_fields['username'] = username

        return self.create_user(pid, password, **extra_fields)



class Users(AbstractUser):

    # This is a custom user model I made for no particular reason.
    # To make it as the User model of this project, I have added 
    #  it as AUTH_USER_MODEL = "users.Users" in settings.py of Main project Folder
    pid = models.CharField(max_length=6, blank=False, null=False, default="000000", unique=True)
    username = models.CharField(max_length=150, blank=True, null=True, unique=True)
    email = models.EmailField(blank=True, default="abc@abc.com")
    role = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.username} - {self.role}"

    USERNAME_FIELD = 'username'  # Use 'username' for authentication
    REQUIRED_FIELDS = ['pid']  # Include 'pid' in required fields for createsuperuser


    objects = CustomUserManager()
    # above line sets manager for this very model.
    # A manager in Django is a class that provides methods to interact with the database for a particular model. 


    def __str__(self):
        return self.pid


# Super User Details:
# UserName: larson
# PID: 100000
# Password: larson
# email: larson@larson.com 