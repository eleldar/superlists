from .models import User, Token

class PasswordlessAuthenticationBackend(object):
    """серверный процессор беспарольной аутентификации"""

    def authenticate(self, request, uid):
        """авторизовать"""
        try:
            token = Token.objects.get(uid=uid)
            return User.objects.get(email=token.email)
        except User.DoesNotExist:
            return User.objects.create(email=token.email)
        except Token.DoesNotExist:
            return
