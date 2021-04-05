from django.template.loader import render_to_string
from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from ..models import Item, List
from ..views import home_page

class HomePageTest(TestCase):
    '''тест домашней страницы'''

    def test_uses_home_template(self):
        '''тест: используется домашний шаблон'''
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html') # тестовый клиент Django;
                                                             # имеет недостатки (т.к. есть разница между полноизолированными модульными тестами и интегрированными тестами)

class ListAndItemModelTest(TestCase):
    '''тест модели элемента списка'''
    def test_saving_and_retrieving_items(self):
        '''тест сохранения и получения элементов списка'''
        list_ = List() # cоздаем новый объект List и назначаем ему каждый элемент
        list_.save()

        first_item = Item()
        first_item.text = 'Первый (какой-нибудь) элемент списка'
        first_item.list = list_ # присваиваем свойству list
        first_item.save()

        second_item = Item()
        second_item.text = 'Второй элемент списка'
        second_item.list = list_ # присваиваем свойству list
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_) # проверяем, что список должным образом сохранен

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'Первый (какой-нибудь) элемент списка')
        self.assertEqual(first_saved_item.list, list_) # проверяем, что первый элемент сохранил связь со списком сохранен
        self.assertEqual(second_saved_item.text, 'Второй элемент списка')
        self.assertEqual(second_saved_item.list, list_)  # проверяем, что второй элемент сохранил связь со списком

class ListViewTest(TestCase):
    '''тест представления списка'''
    def test_uses_list_template(self):
        '''тест: используется шаблон списка'''
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'lists/list.html') # assertTemplateUsed – одна из наиболее 
                                                             # полезных функций тестового клиента Django

    def test_displays_only_items_for_that_list(self):
        '''тест: отображаются элементы только для этого списка'''
        correct_list = List.objects.create()
        Item.objects.create(text='Элемент 1', list=correct_list)
        Item.objects.create(text='Элемент 2', list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text='Другой элемент 1 из списка', list=other_list)
        Item.objects.create(text='Другой элемент 2 из списка', list=other_list)

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, 'Элемент 1')
        self.assertContains(response, 'Элемент 2')
        self.assertNotContains(response, 'Другой элемент 1 из списка')
        self.assertNotContains(response, 'Другой элемент 2 из списка')

    def test_passes_correct_list_to_template(self):
        '''тест: передается список в html-шаблон'''
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list) # response.context представляет контекст, который мы собираемся передать
                                                                 # в функцию генерирования HTML render – тестовый клиент Django помещает его в объект response,
                                                                 # чтобы помочь с тести­рованием

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
        # Этот тест должен сообщать, что представление переадресовывает 
        # на URL-адрес конкретного нового списка, который оно только что 
        # создало
        response = self.client.post('/lists/new', data={'item_text': 'Новый элемент списка'}) # /new без закрывающей косой черты.
                                                                                              # используется форма записи, суть которой в том, 
                                                                                              # что URL-адреса без такой черты являются 
                                                                                              # URL-адресами «действия», которое изменяет базу данных
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/') # заменяет 2 утверждения:
                                                                 # 1. переадресацию
                                                                 # 2. соответствие адресов

class NewItemTest(TestCase):
    '''тест нового элемента списка'''

    def test_can_save_a_POST_request_to_an_existing_list(self):
        '''тест: можно сохранить POST-запрос в существующий список'''
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': 'Новый элемент для существующего списка'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'Новый элемент для существующего списка')
        self.assertEqual(new_item.list, correct_list)

    def test_redirect_to_list_view(self):
        '''тест: переадресуется в представление списка'''
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': 'Новый элемент для существующего списка'}
        )
        self.assertRedirects(response, f'/lists/{correct_list.id}/')
