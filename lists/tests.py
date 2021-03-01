from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

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

    def test_home_page_returns_correct_html(self):
        '''домашняя страница возвращает правильный html'''
        request = HttpRequest()       # 1; бъект HttpRequest , то есть то, что Django увидит, когда браузер пользователя запросит страницу
        response = home_page(request) # 2; передаем объект HttpRequest представлению home_page , которое дает отклик
        html = response.content.decode('utf8') # 3; извлекаем содержимое .content отклика
        self.assertTrue(html.startswith('<html>')) # 4; нужно, чтобы она начиналась с тега <html> , который закрывается в конце 
        self.assertIn('<title>To-Do lists</title>', html) # 5; хотим разместить тег <title> со словами «to-do lists» где-нибудь в середине
        self.assertTrue(html.endswith('</html>')) # 4; закрытие тега в конце

