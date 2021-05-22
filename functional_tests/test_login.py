from django.core import mail
from selenium.webdriver.common.keys import Keys
import re

from .base import FunctionalTest

TEST_EMAIL = 'eleldar@mail.ru'
SUBJECT = 'Ваша ссылка для доступа к списку дел'

class LoginTest(FunctionalTest):
    """тест регистрации в системе """

    def test_can_get_email_link_to_log_in(self):
        """"тест: можно получить ссылку по почте для регистрации"""
        # Лена заходит на сайт суперсписков и впервые замечает раздел "войти" в навигационной панели
        # Он говорит ей ввести свой адрес электронной почты, что она и делает
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('email').send_keys(TEST_EMAIL)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        # Появляется сообщение, которое говорит, что ей на почту было выслано электронное письмо
        self.wait_for(lambda: self.assertIn(
            'Проверьте свою почту',
            self.browser.find_element_by_tag_name('body').text
        ))

        # Лена проверяет свою почту и находит сообщение
        email = mail.outbox[0] # Django предоставляет доступ к любым электронным письмам, которые сервер пытается отправить через атрибут mail.outbox
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(email.subject, SUBJECT)

        # Оно содержит ссылку на url-адрес
        self.assertIn('Используйте эту ссылку для входа', email.body)
        url_search = re.search(r'http://.+/.+$', email.body) # ищем ссылку в теле письма
        if not url_search:
            self.fail(f'URL-адрес отсутствует в письме:\n{email.body}')
        url = url_search.group(0) # ссылка
        self.assertIn(self.live_server_url, url) # поиск адреса сайта в ссылке

        # Лена нажимает на ссылку
        self.browser.get(url)

        # Она зарегистрирована в системе!
        self.wait_for(
            lambda: self.browser.find_element_by_link_text('Выйти')
        )
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(TEST_EMAIL, navbar.text)

        # Теперь она выходит из системы
        self.browser.find_element_by_link_text('Выйти').click()

        # Она вышла из системы
        self.wait_for(
            lambda: self.browser.find_element_by_name('email')
        )
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(TEST_EMAIL, navbar.text)

