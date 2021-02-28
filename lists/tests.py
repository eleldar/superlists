from django.test import TestCase
from django.urls import resolve
from .views import home_page # 2; функция представления, которую мы собираемся написать далее, и она вернет фактический HTML, который
                             # нам нужен. Из оператора import вы видите, что мы планируем со-
                             # хранить ее в lists/views.py.

class HomePageTest(TestCase):
    '''тест домашней страницы'''

    def test_root_url_resolves_to_home_page_view(self):
        '''тест: корневой url преобразуется в представление домашней страницы'''
        found = resolve('/') # 1; функция, которую Django использует внутренне для
                             # преобразования URL-адреса и нахождения функций представления,
                             # в соответствие которым они должны быть поставлены
        self.assertEqual(found.func, home_page) # проверяем, чтобы resolve , когда ее вызывают с «/», то есть корнем сайта,
                                                # нашла функцию под названием home_page .
