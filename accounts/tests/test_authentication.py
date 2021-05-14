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

class GetUserTest(TestCase):
    """тест получения пользователя"""

    def test_get_user_by_email(self):
        """тест: получает пользователя по адресу электронной почты"""
        User.objects.create(email='1@1.com')
        desired_user = User.objects.create(email='eleldar@mail.ru')
        found_user = PasswordlessAuthenticationBackend().get_user('eleldar@mail.ru')
        self.assertEqual(found_user, desired_user)

    def test_returns_None_if_no_user_with_that_email(self):
        """тест: возвращается None, если нет пользователя с таким адресом эл.почты"""
        self.assertIsNone(PasswordlessAuthenticationBackend().get_user('eleldar@mail.ru'))
