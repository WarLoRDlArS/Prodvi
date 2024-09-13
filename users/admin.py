from django.contrib import admin

# # Register your models here.


# stuff to do



# Thanks for clarifying that `pid` is an additional field and not the primary key or username. Given this, the issue with the `create_superuser` method in your `CustomUserManager` is that it expects `pid` as a required positional argument, but Django's `createsuperuser` management command doesn't automatically pass it.

# To resolve this, you'll need to adjust the `create_superuser` method and possibly ensure your `createsuperuser` command is properly set up to handle additional fields.

# ### Steps to Fix the Issue

# #### 1. **Update `create_superuser` Method**

# You should ensure that `pid` is not required when calling `create_superuser` from the Django management command but still handle it appropriately.

# Here's an updated approach to the `create_superuser` method:

# ```python
# class CustomUserManager(BaseUserManager):
#     def create_user(self, pid, password=None, **extra_fields):
#         if not pid:
#             raise ValueError('The PID field must be set')
#         user = self.model(pid=pid, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, pid=None, password=None, **extra_fields):
#         # No need to enforce pid requirement here; it can be None or provided.
#         if password is None:
#             raise ValueError('Superusers must have a password.')
        
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
        
#         # Ensure that the user is created with required superuser status
#         return self.create_user(pid, password, **extra_fields)
# ```

# This way, `pid` is not a required positional argument in `create_superuser` but can be provided if needed.

# #### 2. **Customize the `createsuperuser` Command**

# Since `pid` is an additional field, you need to ensure it's handled correctly by customizing the `createsuperuser` command to prompt for `pid`. This involves creating a custom management command that extends Django’s `createsuperuser`.

# Create a file `Prodvi/users/management/commands/createsuperuser.py` with the following content:

# ```python
# from django.contrib.auth.management.commands import createsuperuser
# from django.core.management import CommandError
# from django.utils.text import capfirst

# class Command(createsuperuser.Command):
#     def add_arguments(self, parser):
#         super().add_arguments(parser)
#         parser.add_argument('--pid', default=None, help='Specify the PID for the superuser.')

#     def handle(self, *args, **options):
#         pid = options.get('pid')
#         if not pid:
#             raise CommandError('You must specify a PID for the superuser using --pid.')

#         # Pass the pid argument to the superuser creation process
#         options['username'] = pid  # Adjust this if pid should not be used as the username
#         super().handle(*args, **options)
# ```

# In this custom command, we:
# 1. Add an argument for `pid`.
# 2. Ensure `pid` is provided when running the command.
# 3. Pass `pid` to the creation process.

# #### 3. **Ensure Admin Compatibility**

# Ensure your admin setup accommodates the custom user model. If you have specific fields like `pid`, ensure they are included in forms and list displays.

# Here’s a basic example of how to set up your admin interface:

# ```python
# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import Users

# class CustomUserAdmin(UserAdmin):
#     model = Users
#     # Customize the fields displayed in the admin interface
#     list_display = ('pid', 'is_staff', 'is_superuser', 'is_active')
#     fieldsets = UserAdmin.fieldsets + (
#         (None, {'fields': ('pid',)}),
#     )
#     add_fieldsets = UserAdmin.add_fieldsets + (
#         (None, {'fields': ('pid',)}),
#     )

# admin.site.register(Users, CustomUserAdmin)
# ```

# ### Summary

# 1. **Update** the `create_superuser` method to make `pid` optional.
# 2. **Create** a custom `createsuperuser` command to handle additional fields.
# 3. **Ensure** admin compatibility with your custom user model.

# With these adjustments, your `createsuperuser` command should work correctly with your custom user model. If you have further issues or questions, feel free to ask!