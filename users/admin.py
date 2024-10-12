from django.contrib import admin

# # Register your models here.

from .models import Users

class UsersAdmin( admin.ModelAdmin ):
    list_display = ('pid', 'username', 'is_staff', 'is_superuser')
    search_fields = ('pid', 'username')
    ordering = ('pid', )

admin.site.register(Users, UsersAdmin)