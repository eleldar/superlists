from django.test import TestCase
from unittest.mock import patch, call
from .. import views
from .. models import Token

SUCCESS_MESSAGE = "Проверьте свою почту. В сообщении находится ссылка, которая позволит войти на сайт."

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
        self.assertEqual(message.message, SUCCESS_MESSAGE)
        self.assertEqual(message.tags, "success")



# Cледующий тест (тест с имитациями) не срабатывает, потому что больше не вызываем messages.success,
# а вызываем messages.add_message с другим количеством аргументов.
# Использование имитаций может привести к сильно связанной реализации.
# Лучше тестировать поведение, а не детали реализации. Тестируйте то, что происходит,
# а не то, как вы это делаете. Нередко имитации допускают слишком много ошибок на стороне «как»,
# а не на стороне «что».

#    @patch('accounts.views.messages')
#    def test_adds_success_message_with_mock(self, mock_messages):
#        """имитируем модуль messages; проверяем, что функция messages.success вызвана с правильными аргументами: 
#           первоначальный запрос и сообщение, которое мы хотим."""
#        response = self.client.post('/accounts/send_login_email',
#            data={'email': 'eleldar@mail.ru'
#        })
#
#        self.assertEqual(mock_messages.success.call_args,
#            call(response.wsgi_request, SUCCESS_MESSAGE)
#        )

class LoginViewTest(TestCase):
    """тест представления входа в систему"""

    def test_redirects_to_home_page(self):
        """тест: переадресуется на домашнюю страницу"""
        response = self.client.get('/accounts/login?token=avrwvrgwef21124255')
        self.assertRedirects(response, '/')

    def test_creates_token_associated_with_email(self):
        """тест: создается маркер, связанный с электронной почтой"""
        # проверяет, что маркер, который мы создаем в базе данных, 
        # связан с адресом электронной почты из POST-запроса.
        self.client.post('/accounts/send_login_email',
            data={'email': 'eleldar@mail.ru'}
        )
        token = Token.objects.first()
        self.assertEqual(token.email, 'eleldar@mail.ru')

    @patch('accounts.views.send_mail')
    def test_sends_link_to_login_using_token_uid(self, mock_send_mail):
        """тест: отсылается ссылка на вход в систему, используя uid маркера"""
        # имитируем функцию send_mail , используя декоратор patch;
        # из всех аргументов вызова нас интересует аргумент body
        self.client.post('/accounts/send_login_email',
            data = {'email': 'eleldar@mail.ru'}
        )

        token = Token.objects.first()
        expected_url = f'http://testserver/accounts/login?token={token.uid}'
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertIn()
