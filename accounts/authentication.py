import sys
from accounts.models import ListUser, Token

class PasswordlessAuthenticationBackend(object):
    """серверный процессор беспарольной аутентификации"""

    def authenticate(self, request, uid):
        """авторизовать"""
        print('uid', uid, file=sys.stderr)
        if not Token.objects.filter(uid=uid).exists():
            print('токен не найден', file=sys.stderr)
            return None
        token = Token.objects.get(uid=uid)
        print('токен получен', file=sys.stderr)
        try:
            user = ListUser.objects.get(email=token.email)
            print('пользователь получен', file=sys.stderr)
            return user
        except ListUser.DoesNotExist:
            print('новый пользователь', file=sys.stderr)
            return ListUser.objects.create(email=token.email)

    def get_user(self, email):
        """получить пользователя"""
        return ListUser.objects.get(email=email)
