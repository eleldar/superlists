from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.authentication import PasswordlessAuthenticationBackend
from ..models import Token
REQUEST = 'ok'

User = get_user_model()

class AuthenticateTest(TestCase):
    """тест аутентификации"""

    def test_returns_None_if_no_such_token(self):
        """тест: возвращает None, если нет такого маркера"""
        result = PasswordlessAuthenticationBackend().authenticate(REQUEST,
            'не-существующий-токен'
        )
        self.assertIsNone(result)

    def test_returns_new_user_with_correct_email_if_token_exists(self):
        """тест: возвращает нового пользователя с правильной электронной почтой, если есть маркер"""
        email = 'eleldar@mail.ru'
        token = Token.objects.create(email=email)
        user = PasswordlessAuthenticationBackend().authenticate(REQUEST, token.uid)
        new_user = User.objects.get(email=email)
        self.assertEqual(user, new_user)

    def test_returns_existing_user_with_correct_email_if_token_exists(self):
        """тест: возвращает существующего пользователя с правильной электронной почтой, если есть маркер"""
        email = 'eleldar@mail.ru'
        existing_user = User.objects.create(email=email)
        token = Token.objects.create(email=email)
        user = PasswordlessAuthenticationBackend().authenticate(REQUEST, token.uid)
        self.assertEqual(user, existing_user)
