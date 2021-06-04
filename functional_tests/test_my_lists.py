from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore
from .base import FunctionalTest
from .server_tools import create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session
from time import sleep


class MyListsTest(FunctionalTest):
    """тест приложения 'Мои списки'"""

    def create_pre_authenticated_session(self, email):
        """создать предварительно аутентифицированный сеанс"""
        if self.staging_server:
            session_key = create_session_on_server(self.staging_server, email)
        else:
            session_key = create_pre_authenticated_session(email)

        ## страницы 404 загружаются быстрее всего!
        self.browser.get(self.live_server_url + "/404_no_such_url/")

        # устанавливаем cookie для первого посещения домена
        self.browser.add_cookie(dict(          # добавляем cookie в браузер
            name=settings.SESSION_COOKIE_NAME, # совпадает с сеансом на сервере
            value=session_key, # при визите на сайт сервер  должен распознать нас как зарегистрированного пользователя
            path="/",
        ))

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        """тест: сохраняются списки зарегистрированных пользователей как 'мои списки'"""
        # Лена является зарегистрированным пользователем
        email = 'eleldar@mail.ru'
        self.create_pre_authenticated_session(email) # аутентификация

        # Лена открывает домашнюю страницу и начинает новый список
        self.browser.get(self.live_server_url) # страница сайта
        self.add_list_item('Продукты') # создаем первый элемент
        self.add_list_item('Мороженное') # создаем второй элемент
        first_list_url = self.browser.current_url # получаем текущий URL

        # Она замечает ссылку на "Мои списки" в первый раз.
        self.browser.find_element_by_link_text('Мои списки').click() # нажимаем на ссылку

        # Она видит, что ее список находится там и назван на основе первого элемента списка
        self.wait_for( # тест: список появляется на странице 'Мои списки'
            lambda: self.browser.find_element_by_link_text('Продукты')
        )
        self.browser.find_element_by_link_text('Продукты').click()
        self.wait_for( # тест: список назван как первый элемент этого списка
            lambda: self.assertEqual(self.browser.current_url, first_list_url)
        )

        # Она решает начать еще один список из одного элемента
        self.browser.get(self.live_server_url) # страница сайта
        self.add_list_item('Книги') # создаем первый и единственный элемент
        second_list_url = self.browser.current_url # получаем текущий URL

        # Под заголовком "Мои списки" появляется ее новый список
        self.browser.find_element_by_link_text('Мои списки').click() # нажимаем на ссылку
        self.wait_for( # тест: список появляется на странице 'Мои списки'
            lambda: self.browser.find_element_by_link_text('Книги')
        )
        self.browser.find_element_by_link_text('Книги').click()
        self.wait_for( # тест: список назван как первый элемент этого списка
            lambda: self.assertEqual(self.browser.current_url, second_list_url)
        )

        # Она выходит из системы. Опция "Мои списки" исчезает
        self.browser.find_element_by_link_text('Выйти').click()
        self.wait_for( # тест: список 'Мои списки' должен быть пустым
            lambda: self.assertEqual(
                self.browser.find_elements_by_link_text('Мои списки'),
                []
        ))
