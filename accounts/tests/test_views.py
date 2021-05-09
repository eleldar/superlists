from django.test import TestCase
from accounts import views

class SendLoginEmailViewTest(TestCase):
    """тест представления, отправляющего сообщение для входа в систему"""

    def test_redirect_to_home_page(self):
        """тест: переадресация на домашнюю страницу"""
        response = self.client.post('/accounts/send_login_email',
            data={'email': 'eleldar@mail.ru'}
        )
        self.assertRedirects(response, '/')

    def test_sends_mail_to_address_from_post(self):
        """тест: отправляется сообщение на адрес из метода post"""
        self.send_mail_called = False

        def fake_send_mail(subject, body, from_email, to_list):
            """поддельная функция send_mail; похожа на реальную функцию send_mail,
            но она всего лишь сохраняет некоторую информацию о том, как ее вызвали, 
            с использованием нескольких переменных, заданных на свойстве self"""
            self.send_mail_called = True
            self.subject = subject
            self.body = body
            self.from_email = from_email
            self.to_list = to_list

        views.send_mail = fake_send_mail # подменяем реальную функцию accounts.views.send_mail поддельной версией – это сводится к простой операции присваивания ей значения

        self.client.post('/accounts/send_login_email',
            data={'email': 'eleldar@mail.ru'}
        )

        self.assertTrue(self.send_mail_called)
        self.assertEqual(self.subject, 'Ваша ссылка для доступа к списку дел')
        self.assertEqual(self.from_email, 'noreply@superlists')
        self.assertEqual(self.to_list, ['eleldar@mail.ru'])
