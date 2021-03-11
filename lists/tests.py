from django.template.loader import render_to_string
from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from .models import Item
from .views import home_page

class HomePageTest(TestCase):
    '''тест домашней страницы'''

    def test_uses_home_template(self):
        '''тест: используется домашний шаблон'''
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html') # тестовый клиент Django;
                                                             # имеет недостатки (т.к. есть разница между полноизолированными модульными тестами и интегрированными тестами)

class ItemModelTest(TestCase):
    '''тест модели элемента списка'''
    def test_saving_and_retrieving_items(self):
        '''тест сохранения и получения элементов списка'''
        first_item = Item()
        first_item.text = 'Первый (какой-нибудь) элемент списка'
        first_item.save()

        second_item = Item()
        second_item.text = 'Второй элемент списка'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'Первый (какой-нибудь) элемент списка')
        self.assertEqual(second_saved_item.text, 'Второй элемент списка')

class ListViewTest(TestCase):
    '''тест представления списка'''
    def test_uses_list_template(self):
        '''тест: используется шаблон списка'''
        response = self.client.get('/lists/uniq-list/')
        self.assertTemplateUsed(response, 'lists/list.html') # assertTemplateUsed – одна из наиболее 
                                                             # полезных функций тестового клиента Django

    def test_displays_all_items(self):
        '''тест: отображаются все элементы списка'''
        Item.objects.create(text='Элемент 1')
        Item.objects.create(text='Элемент 2')

        response = self.client.get('/lists/uniq-list/')

        self.assertContains(response, 'Элемент 1')
        self.assertContains(response, 'Элемент 2')

class NewListTest(TestCase):
    '''тест нового списка'''

    def test_can_save_a_POST_request(self):
        '''тест: можно сохранить post-запрос'''
        self.client.post('/lists/new', data={'item_text': 'Новый элемент списка'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'Новый элемент списка')

    def test_redirect_after_POST(self):
        '''тест: переадресует после post-запроса'''
        response = self.client.post('/lists/new', data={'item_text': 'Новый элемент списка'}) # /new без закрывающей косой черты.
                                                                                              # используется форма записи, суть которой в том, 
                                                                                              # что URL-адреса без такой черты являются 
                                                                                              # URL-адресами «действия», которое изменяет базу данных
        self.assertRedirects(response, '/lists/uniq-list/') # новый метод тестового клиента Django; заменяет 2 утверждения:
                                                            #self.assertEqual(response.status_code, 302)
                                                            #self.assertEqual(response['location'], '/lists/uniq-list/')
