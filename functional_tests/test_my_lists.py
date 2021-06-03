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
        email = 'eleldar@mail.ru'
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_out(email) 

        # Лена является зарегистрированным пользователем
        self.create_pre_authenticated_session(email)
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_in(email)

