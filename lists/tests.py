from django.template.loader import render_to_string
from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from .views import home_page

class HomePageTest(TestCase):
    '''тест домашней страницы'''

    def test_root_url_resolves_to_home_page_view(self):
        '''тест: корневой url преобразуется в представление домашней страницы'''
        found = resolve('/') # функция, которую Django использует внутренне для
                             # преобразования URL-адреса и нахождения функций представления,
                             # в соответствие которым они должны быть поставлены
        self.assertEqual(found.func, home_page) # проверяем, чтобы resolve , когда ее вызывают с «/», то есть корнем сайта,
                                                # нашла функцию под названием home_page .

    def test_home_page_returns_correct_html(self):
        '''домашняя страница возвращает правильный html'''
        response = self.client.get('/') # 1; используется вместо создания объекта HttpRequest вручную и прямого вызова функции представления; используется URL-адрес, который хотим протестировать 
        html = response.content.decode('utf8') # извлекаем содержимое .content отклика
        expected_html = render_to_string('lists/home.html') # преобразует шаблон в HTML-разметку
        self.assertEqual(html, expected_html) # сравнение с тем, что возвращает представление

        self.assertTemplateUsed(response, 'lists/home.html') # 3; позволяет проверить, какой шаблон использовался для вывода отклика как HTML (работает только для откликов, которые были получены тестовым клиентом).
