from django.test import TestCase
from unittest.mock import patch
from accounts import views

class SendLoginEmailViewTest(TestCase):
    """тест представления, отправляющего сообщение для входа в систему"""

    def test_redirect_to_home_page(self):
        """тест: переадресация на домашнюю страницу"""
        response = self.client.post('/accounts/send_login_email',
            data={'email': 'eleldar@mail.ru'}
        )
        self.assertRedirects(response, '/')

    @patch('accounts.views.send_mail') # принимает имя объект; эквивалент ручной подмены send_mail в accounts.views; 
    def test_sends_mail_to_address_from_post(self, mock_send_mail): # внедряет объект-имитацию в тест как аргумент метода тестирования; можно выбрать любое имя
        """тест: отправляется сообщение на адрес из метода post"""
        self.client.post('/accounts/send_login_email', # Вызываем тестируемую функцию как обычно, но ко всему, что есть внутри этого метода тестирования, применяется наша имитация, поэтому представление не вызовет реальный send_mail, вместо этого будет видеть mock_send_mail.
            data={'email': 'eleldar@mail.ru'}
        )

        self.assertEqual(mock_send_mail.called, True) # делаем выводы о том, что произошло с объектомими­тацией во время теста; видим, что он вызывается
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args # распаковываем его различные позиционные и именованные аргументы вызова для исследования того, с чем она была вызвана
        self.assertEqual(subject, 'Ваша ссылка для доступа к списку дел')
        self.assertEqual(from_email, 'noreply@superlists')
        self.assertEqual(to_list, ['eleldar@mail.ru'])

    def test_adds_success_message(self):
        """тест: добавляется сообщение об успехе"""
        response = self.client.post('/accounts/send_login_email',
            data={'email': 'eleldar@mail.ru'},
            follow=True) # передавая follow=True в тестовый клиент получаем возможность исследовать
                         # страницу после переадресации с кодом 302:  исследовать ее контекст на
                         # наличие списка сообщений (который мы должны преобразовать в список,
                         # чтобы он начал вести себя так, как надо) -|
                                                          #          |
        message = list(response.context['messages'])[0]   #   <------|
        self.assertEqual(
            message.message,
            "Проверьте свою почту. В сообщении находится ссылка, которая позволит войти на сайт."
        )
        self.assertEqual(message.tags, "success")