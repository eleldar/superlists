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
        self.assertTemplateUsed(response, 'lists/home.html') # тестовый клиент Django; имеет недостатки (т.к. есть разница между полноизолированными модульными тестами и интегрированными тестами)

    def test_can_save_a_POST_request(self):
        '''тест: можно сохранить post-запрос'''
        response = self.client.post('/', data={'item_text': 'Новый элемент списка'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'Новый элемент списка')

    def test_redirects_after_POST(self):
        '''тест: можно сохранить post-запрос'''
        response = self.client.post('/', data={'item_text': 'Новый элемент списка'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/uniq-list/')

    def test_only_saves_items_when_necessary(self):
        '''тест: сохраняет элементы, только когда нужно'''
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)

    def test_displays_all_list_items(self):
        '''тест: отображаются все элементы списка'''
        Item.objects.create(text='Элемент 1')
        Item.objects.create(text='Элемент 2')

        response = self.client.get('/')

        self.assertIn('Элемент 1', response.content.decode())
        self.assertIn('Элемент 2', response.content.decode())

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

    def test_displays_all_items(self):
        '''тест: отображаются все элементы списка'''
        Item.objects.create(text='Элемент 1')
        Item.objects.create(text='Элемент 2')

        response = self.client.get('/lists/uniq-list/')

        self.assertContains(response, 'Элемент 1')
        self.assertContains(response, 'Элемент 2')
