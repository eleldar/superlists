from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore
from .base import FunctionalTest
from time import sleep

User = get_user_model()

class MyListsTest(FunctionalTest):
    """тест приложения 'Мои списки'"""

    def create_pre_authenticated_session(self, email):
        """создать предварительно аутентифицированный сеанс"""
        user = User.objects.create(email=email)
        session = SessionStore()       # Создаем объект-сеанс в базе данных.
        session[SESSION_KEY] = user.pk # Сеансовый ключ – первичный ключ объекта-пользователя (который фактически представлен его адресом электронной почты)
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session.save()
        ## установить cookie, которые нужны для первого посещения домена.
        ## страницы 404 загружаются быстрее всего!
        self.browser.get(self.live_server_url + "/404_no_such_url/")
        self.browser.add_cookie(dict(          # добавляем cookie в браузер
            name=settings.SESSION_COOKIE_NAME, # совпадает с сеансом на сервере
            value=session.session_key, # при визите на сайт сервер  должен распознать нас как зарегистрированного пользователя
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

