from django.test import TestCase

class SendLoginEmailViewTest(TestCase):
    """тест представления, отправляющего сообщение для входа в систему"""

    def test_redirect_to_home_page(self):
        """тест: переадресация на домашнюю страницу"""
        response = self.client.post('/accounts/send_login_email',
            data={'email': 'eleldar@mail.ru'}
        )
        self.assertRedirects(response, '/')
