from .models import User


class EmailAuthBackend(object):
    def authenticate(self, request,username = None, password = None):
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}
        try:
            
            user=User.objects.get (**kwargs)
            if user. check_password (password):
                return user
            return None
        except User. DoesNotExist:
            return None
    def get_user(self, username):
        try:
            return User.objects.get(pk=username)
        except User.DoesNotExist:
            return None