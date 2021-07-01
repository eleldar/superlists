from django.template.loader import render_to_string
from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.utils.html import escape # метод для экранированных символов
from ..models import Item, List
from ..views import home_page
from ..forms import ItemForm, ExistingListItemForm, EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR
from unittest import skip
from unittest.mock import patch, Mock
from django.contrib.auth import get_user_model
import unittest
from lists.views import new_list2
User = get_user_model()


class HomePageTest(TestCase):
    '''тест домашней страницы'''

    def test_uses_home_template(self):
        '''тест: используется домашний шаблон'''
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')


    def test_home_page_uses_item_form(self):
        '''тест: домашняя страница использует форму для элемента'''
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm) # проверяет, что форма соответствует классу ItemForm


class ListViewTest(TestCase):
    '''тест представления списка'''
    def test_uses_list_template(self):
        '''тест: используется шаблон списка'''
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'lists/list.html')

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

    def test_can_save_a_POST_request_to_an_existing_list(self):
        '''тест: можно сохранить POST-запрос в существующий список'''
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f'/lists/{correct_list.id}/',
            data={'text': 'Новый элемент для существующего списка'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'Новый элемент для существующего списка')
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirect_to_list_view(self):
        '''тест: переадресуется в представление списка'''
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f'/lists/{correct_list.id}/',
            data={'text': 'Новый элемент для существующего списка'}
        )
        self.assertRedirects(response, f'/lists/{correct_list.id}/')

    def post_invalid_input(self):
        '''отправляет недопустимый ввод'''
        # Создав небольшую вспомогательную функцию post_invalid_input , мы
        # можем сделать четыре отдельных теста без дублирования большого числа
        # строк исходного кода.
        list_ = List.objects.create()
        return self.client.post(f'/lists/{list_.id}/', data={'text':''})

    def test_for_invalid_input_nothing_saved_to_db(self):
        '''тест на недопустимый ввод: ничего не сохраняется в БД'''
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_renders_list_template(self):
        '''тест на недопустимый ввод: отображается шаблон списка'''
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_for_invalid_input_shows_error_on_page(self):
        '''тест на недопустимый ввод: на странице показывается ошибка'''
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_displays_item_form(self):
        '''тест отображения формы для элемента'''
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertIsInstance(response.context['form'], ExistingListItemForm)
        self.assertContains(response, 'name="text"')

    def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
        '''тест: ошибки вализации повторяющегося элемена оканчиваются на странице списков'''
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='проверочный текст')
        response = self.client.post(
            f'/lists/{list1.id}/',
            data={'text': 'проверочный текст'}
        )

        expected_error = escape(DUPLICATE_ITEM_ERROR)

    def test_for_invalid_input_passes_form_to_template(self):
        '''тест на недопустимый ввод: форма передается в шаблон'''
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ExistingListItemForm)

class NewListViewIntegratedTest(TestCase):
    '''интегрированный тест нового представления списка'''

    def test_can_save_a_POST_request(self):
        '''тест: можно сохранить post-запрос'''
        self.client.post('/lists/new', data={'text': 'Новый элемент списка'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'Новый элемент списка')

    def test_redirect_after_POST(self):
        '''тест: переадресует после post-запроса'''
        # Этот тест должен сообщать, что представление переадресовывает 
        # на URL-адрес конкретного нового списка, который оно только что 
        # создало
        response = self.client.post('/lists/new', data={'text': 'Новый элемент списка'}) # /new без закрывающей косой черты.
                                                                                              # используется форма записи, суть которой в том, 
                                                                                              # что URL-адреса без такой черты являются 
                                                                                              # URL-адресами «действия», которое изменяет базу данных
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/') # заменяет 2 утверждения:
                                                                 # 1. переадресацию
                                                                 # 2. соответствие адресов

    def test_for_invalid_input_renders_home_template(self):
        '''тест на недопустимый ввод: отображает домашний шаблон'''
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/home.html')

    def test_validation_errors_are_shown_on_home_page(self):
        '''тест: ошибки валидации выводятся на домашней странице'''
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_for_invalid_input_passes_form_to_template(self):
        '''тест на недопустимый ввод: форма передается в шаблон'''
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_invalid_list_items_arent_saved(self):
        '''тест: сохраняются недопустимые элементы списка'''
        self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

    @unittest.skip
    def test_list_owner_is_saved_if_user_is_authenticated(self):
        '''тест:для списка сохраняется владелец, если пользователь аутентифицирован'''
        user = User.objects.create(email='1@1.com')
        self.client.force_login(user) # force_login - тестовый клиент выполняет запросы с зарегистрированным пользователем
        self.client.post('/lists/new', data={'text': 'Новый элемент списка'})
        list_ = List.objects.first()
        self.assertEqual(list_.owner, user)


class MyListsTest(TestCase):
    '''тест приложения Мои списки'''

    def test_my_lists_url_renders_my_lists_template(self):
        '''тест: переход по ссылке отображает шаблон'''
        User.objects.create(email='1@1.com')
        response = self.client.get('/lists/users/1@1.com/')
        self.assertTemplateUsed(response, 'lists/my_lists.html')

    def test_passes_correct_owner_to_template(self):
        '''тест: передается правильный владелец в шаблон'''
        User.objects.create(email='wrong@owner.com')
        correct_user = User.objects.create(email='1@1.com')
        response = self.client.get('/lists/users/1@1.com/')
        self.assertEqual(response.context['owner'], correct_user)

@patch('lists.views.NewListForm') # имитируем класс NewListForm; будет использоваться во всех тестах, поэтому имитируем его на уровне класса
class NewListViewUnitTest(unittest.TestCase): # TestCase сильно упрощает написание интегрированных тестов
    '''модульный тест нового представления списка'''

    def setUp(self):
        '''установка'''
        self.request = HttpRequest()
        self.request.POST['text'] = 'Новый элемент списка' # для базового POST-запроса вместо тестового клиента Django
        self.request.user = Mock()

    def test_passes_POST_data_to_NewListForm(self, mockNewListForm):
        '''тест: передаются POST-данные в новую форму списка'''
        new_list2(self.request)
        mockNewListForm.assert_called_once_with(data=self.request.POST) # проверка на правильную инициализацию NewListForm

    def test_saves_form_with_owner_if_form_valid(self, mockNewListForm):
        '''тест: сохраняет форму с владельцем, если форма допустима'''
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = True
        new_list2(self.request)
        mock_form.save.assert_called_once_with(owner=self.request.user)

    @patch('lists.views.redirect') # имитация функции переадресации на уровне метода
    def test_redirects_to_form_returned_object_if_form_valid(
        self, mock_redirect, mockNewListForm # имитация переадресации внедряется перед mockNewListForm
    ):
        '''тест: переадресует в возвращаемый формой объект при допустимой форме'''
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = True # указываем, что тестируем случай, где форма допустима

        response = new_list2(self.request)

        self.assertEqual(response, mock_redirect.return_value) # проверка того, что отклик из представления является результатом функции redirect
        mock_redirect.assert_called_once_with(str(mock_form.save.return_value)) # проверка того, что функция переадресации была вызвана объектом, который форма возвращает при выполнении save
