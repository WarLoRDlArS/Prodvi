from django.contrib.auth.backends import BaseBackend
from .models import Users


class CustomBackend(BaseBackend):
    def authenticate(self, request, pid=None, password=None, **kwargs): 
        try:
            user = Users.objects.get(pid=pid)
            if user.check_password(password):
                return user
        except Users.DoesNotExist: 
            return None
            
    def get_user(self, user_id):
        try:
            return Users.objects.get(pk=user_id)
            # since pid is not a primary key, get_user requires a primarykey, so i was comparing primary key with pid and so it was not authenticating.
            # setting to 'Users.objects.get(pk=user_id)' fixed it
        except Users.DoesNotExist:
            return None
