from django.core import mail
from selenium.webdriver.common.keys import Keys
import os
import poplib
import email as pop_email
from email.header import decode_header
import re
import time
from .base import FunctionalTest

SUBJECT = 'Ваша ссылка для доступа к списку дел'

class LoginTest(FunctionalTest):
    """тест регистрации в системе """
    def wait_for_email(self, test_email, subject):
        '''ожидание электронного сообщения'''
        if not self.staging_server:
            email = mail.outbox[0]
            self.assertIn(test_email, email.to)
            self.assertEqual(email.subject, subject)
            return email.body
        email_id = None
        start = time.time()
        inbox = poplib.POP3_SSL('pop.mail.yahoo.com')
        try:
            inbox.user(test_email)
            inbox.pass_(os.environ['YAHOO_PASSWORD'])
            while time.time() - start < 160:
                # получаем 10 новых сообщений
                count, _ = inbox.stat()
                for i in reversed(range(max(1, count - 10), count + 1)):
                    print('получение сообщения', i)
                    _, lines, __ = inbox.retr(i)
                    # для получения темы письма
                    raw_email  = b"\n".join(lines)
                    parsed_email = pop_email.message_from_bytes(raw_email)
                    sub_from_mail = decode_header(parsed_email.get('Subject'))
                    sub_decode = sub_from_mail[0][0].decode(sub_from_mail[0][1])
                    # для получения тела письма
                    lines = [l.decode('utf8') for l in lines]
                    if subject == sub_decode:
                        email_id = i
                        body = '\n'.join(lines)
                        return body
                time.sleep(5)
        finally:
            if email_id:
                inbox.dele(email_id)
            inbox.quit()


    def test_can_get_email_link_to_log_in(self):
        """"тест: можно получить ссылку по почте для регистрации"""
        # Лена заходит на сайт суперсписков и впервые замечает раздел "войти" в навигационной панели
        # Он говорит ей ввести свой адрес электронной почты, что она и делает
        if self.staging_server:
            test_email = 'intrnttst@yahoo.com'
        else:
            test_email = 'eleldar@mail.ru'
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('email').send_keys(test_email)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        # Появляется сообщение, которое говорит, что ей на почту было выслано электронное письмо
        self.wait_for(lambda: self.assertIn(
            'Проверьте свою почту',
            self.browser.find_element_by_tag_name('body').text
        ))

        # Лена проверяет свою почту и находит сообщение
        body = self.wait_for_email(test_email, SUBJECT)

        # Оно содержит ссылку на url-адрес
        self.assertIn('Используйте эту ссылку для входа', body)
        url_search = re.search(r'http://.+/.+$', body) # ищем ссылку в теле письма
        if not url_search:
            self.fail(f'URL-адрес отсутствует в письме:\n{body}')
        url = url_search.group(0) # ссылка
        self.assertIn(self.live_server_url, url) # поиск адреса сайта в ссылке

        # Лена нажимает на ссылку
        self.browser.get(url)

        # Она зарегистрирована в системе!
        self.wait_to_be_logged_in(email=test_email)

        # Теперь она выходит из системы
        self.browser.find_element_by_link_text('Выйти').click()

        # Она вышла из системы
        self.wait_to_be_logged_out(email=test_email)
