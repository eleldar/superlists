from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserModelTest(TestCase):
    """тест модели пользователя"""

    def test_user_is_valid_with_email_only(self):
        """тест: пользователь допустим только с электронной почтой"""
        user = User(email="a@b.com")
        user.full_clean() # не должно поднять исключение

    def test_email_is_primary_key(self):
        """тест: электронная почта явялется первичным ключом"""
        user = User(email="a@b.com")
        self.assertEqual(user.pk, 'a@b.com')
